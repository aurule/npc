from collections import defaultdict
from .util import OutOfBoundsError

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
        self.problems = ['Not validated']

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

            The "description" and "path" keys are not arrays, so this method
            will return the entire value.
        """
        if key in self.STRING_TAGS:
            return self[key]

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
            A slice of the key's array including all elements except the first.
            May be empty.

            The "description" and "path" keys are not arrays, so this method
            will return the entire value.
        """
        if key in self.STRING_TAGS:
            return self[key]

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
        if not self.has_items('type'):
            self.problems.append("Missing type")
        if not self.has_items('name'):
            self.problems.append("Missing name")

        if self.type_key == "changeling":
            self._validate_changeling(strict=strict)

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
            * zero or one entitlement is present

        Any errors are added to the problems list.

        Returns:
            None
        """
        if not self.has_items('seeming'):
            self.problems.append("Missing seeming")
        if not self.has_items('kith'):
            self.problems.append("Missing kith")
        if self.has_items('court', 2):
            self.problems.append("Multiple courts: {}".format(', '.join(self['court'])))
        if self.has_items('motley', 2):
            self.problems.append("Multiple motleys: {}".format(', '.join(self['motley'])))
        if self.has_items('entitlement', 2):
            self.problems.append("Multiple entitlements: {}".format(', '.join(self['entitlement'])))

    def has_items(self, key, threshold=1):
        """
        Get whether there are a certain number of values for key

        Args:
            key (str): The key to check
            threshold (int): The number of values that must be in key

        Raises:
            OutOfBoundsError if threshold is below 1

        Returns:
            True if key is present and has at least as many values in its list
            as threshold. False if not.
        """
        if threshold < 1:
            raise OutOfBoundsError

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
        Build a large string of tag data

        Returns:
            A string containing tags that when parsed will recreate the data in
            this character object.
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
