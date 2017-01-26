"""
Helper functions shared between the other modules
"""

import re
import json
import sys
from os import getcwd, path
from collections import defaultdict
from subprocess import run

def load_json(filename):
    """
    Parse a JSON file

    First remove all comments, then use the standard json package

    Comments look like :
        // ...
    or
        /*
        ...
        */

    Args:
        filename (str): Path of the file to load

    Returns:
        List or dict from `json.loads()`
    """
    comment_re = re.compile(
        r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    with open(filename) as json_file:
        content = ''.join(json_file.readlines())

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        # Return parsed json
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as err:
            nicestr = "Bad syntax in '{0}' line {2} column {3}: {1}"
            err.nicemsg = nicestr.format(filename, err.msg, err.lineno, err.colno)
            raise err
        except OSError as err:
            err.nicemsg = "Could not load '{0}': {1}".format(filename, err.strerror)
            raise err

def error(*args, **kwargs):
    """
    Print an error message to stderr.

    Args:
        Same as print()
    """
    print(*args, file=sys.stderr, **kwargs)

def flatten(thing):
    """
    Flatten a non-homogenous list

    Example:
        >>> flatten([1, 2, [3, [4, 5]], 6, [7, 8]])
        [1, 2, 3, 4, 5, 6, 7, 8]

    Args:
        thing (list): The list to flatten. Items can be lists or other types.

    Yields:
        Items from the list and any lists within it, as though condensed into a
            single, flat list.
    """
    for item in thing:
        if hasattr(item, '__iter__') and not isinstance(item, str):
            for flattened_item in flatten(item):
                yield flattened_item
        else:
            yield item

def find_campaign_root():
    """
    Determine the base campaign directory

    Walks up the directory tree until it finds the '.npc' campaign config
    directory, or hits the filesystem root. If the `.npc` directory is found,
    its parent is assumed to be the campaign's root directory. Otherwise, the
    current directory of the command invocation is used.

    Returns:
        Directory path to the campaign.
    """
    current_dir = getcwd()
    base = current_dir
    old_base = ''
    while not path.isdir(path.join(base, '.npc')):
        old_base = base
        base = path.abspath(path.join(base, path.pardir))
        if old_base == base:
            return current_dir
    return base

def open_files(*files, prefs=None):
    """
    Open a list of files with the configured editor

    Args:
        files (str): List of file paths to open
        prefs (Settings): Settings object to supply the editor name

    Returns:
        CompletedProcess object as per subprocess.run
    """
    return run(args=[prefs.get("editor"), *files])

class Singleton(type):
    """
    Metaclass for creating singleton classes.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Result:
    """
    Data about the result of a subcommand

    Attributes:
        success (bool): Whether the subcommand ran correctly
        openable (list): Paths to files which were changed by or are relevant to
            the subcommand
        errcode (int): Error code indicating the type of error encountered.

            Error codes:
            0 -- Everything's fine
            1 -- Tried to create a file that already exists
            2 -- Latest plot and session files have different numbers
            3 -- Feature is not yet implemented
            4 -- Filesystem error
            5 -- Unrecognized format
            6 -- Invalid option
            7 -- Unrecognized template
            8 -- Missing required file
        errmsg (str): Human-readable error message. Will be displayed to the
            user.
        printable (list[str]): List of strings that detail changes made. Safe to
            leave blank.
    """
    def __init__(self, success, **kwargs):
        super(Result, self).__init__()
        self.success = success
        self.openable = kwargs.get('openable')
        self.errcode = kwargs.get('errcode', 0)
        self.errmsg = kwargs.get('errmsg', '')
        self.printable = kwargs.get('printable', [])

    def __str__(self):
        if self.success:
            return "Success"
        return self.errmsg

    def __bool__(self):
        return self.success

class Character(defaultdict):
    """
    Object to hold and access data for a single character

    Basically a dictionary with some helper methods. When accessed like a dict,
    missing keys will return an empty array instead of throwing an exception.
    The "description" and "path" keys are special: they will always contain a
    string.
    """

    GROUP_TAGS = (
        'court', 'motley', 'entitlement', # changeling
        'group'                           # universal
    )
    """tuple (str): Group-like tags. These all accept an accompanying `rank` tag."""

    STRING_TAGS = ('description', 'path')
    """
    tuple (Str): String-only data. These are stored as plain strings and do not, in
        fact, come from a tag at all.
    """

    def __init__(self, attributes=None, **kwargs):
        """
        Create a new Character object.

        When supplying values through `attributes` or `**kwargs`, remember that
        almost everything needs to be in a list. The exceptions are the
        "description" and "path" keys, which must be strings, and the "rank"
        key, which is special. It is a dict of dicts, and the members of that
        dict are lists. When in doubt, it's safer to build the object using the
        append and append_rank methods.

        Args:
            attributes (dict): Dictionary of attributes to insert into the
                Character.
            **kwargs: Named arguments will be added verbatim to the new
                Character. Keys here will overwrite keys of the same name from
                the `attributes` arg.
        """
        super().__init__(list)
        for key in self.STRING_TAGS:
            self[key] = ''
        self['rank'] = defaultdict(list)

        if attributes is not None:
            self.update(attributes)
        self.update(kwargs)
        self.problems = []

    @property
    def valid(self):
        """
        bool: Whether this character is valid based on the most recent results
            of validate().
        """
        return len(self.problems) == 0

    @property
    def type_key(self):
        """
        str: Type key for this character or None if no type is present
        """
        try:
            return self.get_first('type').lower()
        except AttributeError:
            return None

    def get_first(self, key, default=None):
        """
        Get the first element from the named key.

        Args:
            key (str): Name of the key
            default (any): Value to return if the key is not present or has no
                values

        Returns:
            The first value in the named key's array. Usually a string. Returns
            default if the key is not present or has no values.

            The "description" key is not an array, so this method will return the
            entire description.
        """
        if key in self.STRING_TAGS:
            return self[key]

        try:
            return self[key][0]
        except IndexError:
            return default

    def get_remaining(self, key, default=None):
        """
        Get all non-first elements from the named key.

        Args:
            key (str): Name of the key
            default (any): Value to return if the key is not present or has no
                values

        Returns:
            A slice of the key's array including all elements but the first.
            May be empty.

            The "description" key is not an array, so this method will return the
            entire description.
        """
        if key in self.STRING_TAGS:
            return self[key]

        if default is None:
            default = []

        try:
            return self[key][1:]
        except IndexError:
            return default

    def append(self, key, value):
        """
        Add a value to a key's array.

        The "description" key is not an array, so `value` will be appended to
        the existing description.

        Args:
            key (str): Name of the key
            value (any): Value to add to the key's list

        Returns:
            This character object. Convenient for chaining.
        """
        if key in self.STRING_TAGS:
            self[key] += value
        else:
            self[key].append(value)

        return self

    def append_rank(self, group, value):
        """
        Add a rank value for the named group

        Args:
            group (str): Group name
            value (str): Rank name to insert

        Returns:
            This character object. Convenient for chaining.
        """
        self['rank'][group].append(value)
        return self

    def validate(self, strict=False):
        """
        Validate the presence of a few required elements: description and type.

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this Character has no validation problems, false if not.
        """
        self.problems = []
        if not self['description'].strip():
            self.problems.append("Missing description")
        if not self.get_first('type'):
            self.problems.append("Missing type")
        if not self.get_first('name'):
            self.problems.append("Missing name")

        if self.type_key == "changeling":
            self._validate_changeling()

        return len(self.problems) == 0

    def _validate_changeling(self, strict=False):
        """
        Validate the basic elements of a changeling file

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        The following must be true:
            * seeming is present
            * kith is present
            * zero or one court is present
            * zero or one motley is present

        Any errors are added to the problems list.

        Returns:
            None
        """
        if not self.get_first('seeming'):
            self.problems.append("Missing seeming")
        if not self.get_first('kith'):
            self.problems.append("Missing kith")
        if len(self['court']) > 1:
            self.problems.append("Multiple courts: {}".format(', '.join(self['court'])))
        if len(self['motley']) > 1:
            self.problems.append("Multiple motleys: {}".format(', '.join(self['motley'])))

    def has_items(self, key, threshold=1):
        """
        Get whether there are a certain number of values for key

        Args:
            key (str): The key to check
            threshold (int): The number of values that must be in key

        Returns:
            True if key is present and has at least as many values in its list
            as threshold. False if not.
        """
        return len(self[key]) >= threshold

    def copy_and_alter(self, func):
        """
        Copy this character object and change its fields

        Makes a copy of a this object. The function func is called on every
        value and its return value is inserted into the copy.

        Args:
            func (function): Function to apply to every value within the
                original

        Returns:
            Character object containing values from the original after being
            altered by func.
        """
        new_char = Character()
        for attr, values in self.items():
            if attr == 'rank':
                for group, ranks in values.items():
                    for item in ranks:
                        new_char.append_rank(group, func(item))
            elif attr in self.STRING_TAGS:
                new_char.append(attr, func(values))
            else:
                for item in values:
                    new_char.append(attr, func(item))

        return new_char

    def build_header(self):
        """
        description

        type or compound type
        special groups
        groups
        dead
        foreign

        appearance
        """
        lines = []

        def tags_for_all(attrname):
            """Add a tag for every value in attrname"""
            lines.extend(["@{} {}".format(attrname, val) for val in self[attrname]])

        def buffered(attrname, fn):
            """Insert a newline before running fn, but only if attrname exists"""
            if attrname in self:
                lines.append("")
                fn(attrname)

        def add_flag(attrname):
            """Add a bare tag, with no value, as long as attrname exists"""
            if attrname in self:
                lines.append("@{}".format(attrname))

        def tags_or_flag(attrname):
            """Add tags or a flag for attrname, whichever is more appropriate."""
            if attrname in self:
                if len(self[attrname]):
                    tags_for_all(attrname)
                else:
                    add_flag(attrname)

        add_flag('skip')

        first_name = self.get_first('name')
        path = self.get('path')
        if first_name and first_name not in path:
            lines.append("@realname {}".format(first_name))
        lines.extend(["@name {}".format(val) for val in self.get_remaining('name')])

        if self.type_key == 'changeling':
            if 'seeming' in self and 'kith' in self:
                lines.append("@changeling {} {}".format(self.get_first('seeming'), self.get_first('kith')))
            else:
                lines.append("@type Changeling")
                if 'seeming' in self:
                    lines.append("@seeming {}").format(self.get_first('seeming'))
                if 'kith' in self:
                    lines.append("@kith {}").format(self.get_first('kith'))
        else:
            lines.append("@type {}".format(self.get_first('type')))

        tags_for_all('faketype')

        tags_for_all('title')
        tags_or_flag('foreign')
        add_flag('wanderer')
        for tagname in self.GROUP_TAGS:
            for groupname in self[tagname]:
                lines.append("@{} {}".format(tagname, groupname))
                lines.extend(["@rank {}".format(rank) for rank in self['rank'][groupname]])

        buffered('dead', tags_or_flag)
        buffered('appearance', tags_for_all)
        buffered('mask', tags_for_all)
        buffered('mien', tags_for_all)

        tags_for_all('hide')
        tags_for_all('hidegroup')
        tags_for_all('hideranks')

        return self['description'] + "\n".join(lines)
