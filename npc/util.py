"""
Helper functions shared between the other modules
"""

import re
import json
import sys
from collections import defaultdict

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
    """
    def __init__(self, success, **kwargs):
        super(Result, self).__init__()
        self.success = success
        self.openable = kwargs.get('openable')
        self.errcode = kwargs.get('errcode', 0)
        self.errmsg = kwargs.get('errmsg', '')

    def __str__(self):
        if self.success:
            return "Success"
        else:
            return self.errmsg
        return self.errmsg

class Character(defaultdict):
    """
    Object to hold and access data for a single character

    Basically a dictionary with some helper methods. When accessed like a dict,
    missing keys will return an empty array instead of throwing an exception.
    The "description" key is special: it will always contain a string.
    """
    def __init__(self, attributes=None, **kwargs):
        """
        Create a new Character object.

        When supplying values through `attributes` or `**kwargs`, remember that
        almost everything needs to be in a list. The exceptions are the
        "description" key, which must be a string, and the "rank" key, which is
        special. It is a dict of dicts, and the members of that dict are lists.
        When in doubt, it's safer to build the object using the append and
        append_rank methods.

        Args:
            attributes (dict): Dictionary of attributes to insert into the
                Character.
            **kwargs: Named arguments will be added verbatim to the new
                Character. Keys here will overwrite keys of the same name from
                the `attributes` arg.
        """
        super().__init__(list)
        self['description'] = ''
        self['rank'] = defaultdict(list)

        if attributes is not None:
            self.update(attributes)
        self.update(kwargs)
        self.problems = []

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
        if key == "description":
            return self["description"]

        try:
            return self[key][0]
        except IndexError:
            return default

    def get_remaining(self, key):
        """
        Get all non-first elements from the named key.

        Args:
            key (str): Name of the key

        Returns:
            A slice of the key's array including all elements but the first.
            May be empty.

            The "description" key is not an array, so this method will return the
            entire description.
        """
        if key == "description":
            return self["description"]

        return self[key][1:]

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
        if key == "description":
            self["description"] += value
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

    def validate(self):
        """
        Validate the presence of a few required elements: description and type.

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

        if self.get_type_key() == "changeling":
            self._validate_changeling()

        return len(self.problems) == 0

    def _validate_changeling(self):
        """
        Validate the basic elements of a changeling file

        The following must be true:
            * seeming is present
            * kith is present
            * zero or one court is present
            * zero or one motley is present

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

    def is_valid(self):
        """
        Get whether this Character is valid

        This method does not redo the validation, so it should only be called
        when you're sure the object's state has not changed since the last
        validation. When in doubt, call validate instead.

        Returns:
            True if this Character has no validation problems, false if not.
        """
        return len(self.problems) == 0

    def get_type_key(self):
        """
        Get the type key for this character

        The type key is a lower case string made from the first entry under
        'type'.

        Returns:
            The canonical type key for this character as a string, or None if
            no type is present.
        """
        try:
            return self.get_first('type').lower()
        except AttributeError:
            return None
