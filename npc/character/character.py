import npc
from npc.util import OutOfBoundsError, flatten, merge_to_dict

from collections import defaultdict

class Character:
    """
    Object to hold and access data for a single character

    Can be accessed like a dictionary where missing keys will return an empty
    array instead of throwing an exception. The "path" key is special: it will
    always contain a string.

    While values can be accessed directly, it's better practice to use the
    getter and setter methods that are provided, since they automatically
    preserve the internal structure of the dict.
    """

    IMPLICIT_FIELDS = ('description',)
    """
    tuple (Str): Fields without an explicit tag.
    """

    GROUP_TAGS = (
        'court', 'motley', 'entitlement', # changeling
        'pack', 'tribe', 'lodge',         # werewolf
        'group')                          # universal
    """tuple (str): Group-like tags. These all accept an accompanying `rank`
        tag."""

    ADDON_TAGS = ('rank',)
    """tuple (str): Tags whose value relates to a previous tag"""

    FLAGS = ('wanderer', 'skip')
    """tuple (str): Flags whose value is ignored"""

    DATA_FLAGS = ('foreign', 'dead')
    """tuple (str): Flags that can accept an optional value"""

    VALUE_TAGS = (
        'name', 'type', 'faketype', 'title', 'appearance', 'hide', 'hidegroup', 'hideranks', # universal
        'seeming', 'kith', 'mask', 'mien'                                                    # changeling
        )
    """tuple (str): Tags that must have a value. Shortcuts, like @changeling,
        are expanded during parsing and do not appear literally."""

    KNOWN_TAGS = IMPLICIT_FIELDS + GROUP_TAGS + FLAGS + DATA_FLAGS + ADDON_TAGS + VALUE_TAGS
    """tuple (str): All recognized tags. Other, unrecognized tags are fine to
        add and will be ignored by methods that don't know how to handle them."""

    def __init__(self, attributes: dict=None, other_char=None, path=None, **kwargs):
        """
        Create a new Character object.

        Initial tag values can be supplied in three ways depending on what's
        most convenient: an existing character, a dict of attributes, and misc
        keyword arguments. Character tags are copied first, then overwritten by
        values from the attributes dict, then overwritten by values from
        individual keyword args.

        When supplying values through `attributes` or `**kwargs`, remember that
        almost everything needs to be in a list. The exceptions are the "path"
        key, which must be strings, and the "rank" key, which is special. It is
        a dict of dicts, and the members of that dict are lists. When in doubt,
        it's safer to build the object using the append and append_rank methods.

        Args:
            attributes (dict): Dictionary of attributes to insert into the
                Character. If a value is a bare string, it will be converted to
                a list containing that string.
            other_char (Character): Existing character object to copy. Tags from
                that object will be copied verbatim with no changes.
            path (pathlike): Path to the file this character object represents
            **kwargs: Named arguments will be added verbatim to the new
                Character. Keys here will overwrite keys of the same name from
                the `attributes` arg. The values here are not altered at all.
        """
        def wrap_strings(attributes: dict):
            wrapped_attributes = {}
            for key, val in attributes.items():
                if isinstance(val, dict):
                    wrapped_attributes[key] = wrap_strings(val)
                elif isinstance(val, str):
                    wrapped_attributes[key] = [val]
                else:
                    wrapped_attributes[key] = val
            return wrapped_attributes

        self.tags = defaultdict(list)
        self.tags['rank'] = defaultdict(list)
        self.path = path

        self._set_default_type()

        if other_char:
            self.tags.update(other_char.tags)
            self.path = other_char.path

        if attributes:
            attributes = wrap_strings(attributes)
            self.tags.update(attributes)

        self.tags.update(kwargs)

        if self.path is None:
            self.path = ''

        self.problems = ['Not validated']

    def _set_default_type(self):
        """
        Set the default character type

        This is usually a no-op, but subclasses can implement this to set their
        native type.

        After being set, this value will be overwritten by arguments to init.
        """
        pass

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

    @property
    def foreign(self):
        """
        bool: Whether this character has data in its foreign or wanderer tags
        """
        return self.has_items('foreign') or self.has_items('wanderer')

    @property
    def locations(self):
        """
        iter: Non-empty foreign and location names
        """
        return filter(bool, self.tags['foreign'] + self.tags['location'])

    @property
    def has_locations(self):
        """
        bool: Whether this character has non-empty location names
        """
        return len(list(self.locations)) >= 1

    @property
    def description(self):
        """
        str: All description lines joined by newlines.
        """
        return "\n".join(self.tags['description'])


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

            The "path" and "rank" keys are not arrays, so this method behaves
            differently. Passing "path" will return the entire path value, and
            passing "ranks" will return the default.
        """
        if key not in self.tags or key == 'rank':
            return default

        try:
            return self.tags[key][0]
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

            The "path" and "rank" keys are not arrays, so this method behaves
            differently. Passing "path" will return the entire path value, and
            passing "ranks" will return an empty array.
        """
        if key not in self.tags or key == 'rank':
            return []

        return self.tags[key][1:]

    def get_ranks(self, group_name):
        """
        Get all ranks for a named group

        Args:
            group_name (str): Name of the group

        Returns:
            List of rank names for the group, or an empty list if none are present.
        """

        try:
            return self.tags['rank'][group_name]
        except KeyError:
            return []

    def tag_contains(self, key, value):
        """
        See if the entries for key contain value

        The search is case-insensitive. If key is "rank", then
        all rank entries will be tested, regardless of group.

        Args:
            key (str): The key whose entries should be searched
            value (str): The value to search for

        Returns:
            True if key has an entry that contains value, False if not.
        """
        if key not in self.tags:
            return False

        wildcard_search = value == '*'

        if key == 'rank':
            searchme = flatten([self.tags['rank'][g] for g in self.tags['rank']])
            if wildcard_search and len(list(searchme)) > 0:
                return True
        else:
            searchme = self.tags[key]
            if wildcard_search:
                return True

        for searchval in searchme:
            if value in searchval.casefold():
                return True

        return False

    def append(self, key, value):
        """
        Add a value to a key's array.

        Keys marked as string fields are not arrays, so `value` will be
        appended to the existing data.

        Args:
            key (str): Name of the key
            value (any): Value to add to the key's list. If value itself is a
                list, its contents will be appended to our own.

        Returns:
            This character object. Convenient for chaining.
        """
        merge_to_dict(self.tags, key, value)

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
        self.tags['rank'][group].append(value)
        return self

    def merge_all(self, other_dict: dict):
        """
        Add all data from other_dict into this character

        The value for each key in other_dict is appended to our own value for
        that key. If that value is an array, its elements are joined onto our
        own. Otherwise, the value is simply appended.

        This method requires that keys with special formatting like `ranks` are
        formatted appropriately in other_dict.

        Args:
            other_dict (dict): Dict of data to merge

        Returns:
            This character object. Convenient for changing.
        """

        for key, value in other_dict.items():
            if key == 'rank':
                for group_name, group_rank in value.items():
                    merge_to_dict(self.tags['rank'], group_name, group_rank)
            else:
                self.append(key, value)

        return self

    def validate_tag_present_and_filled(self, tag: str):
        """
        Validate that a tag has a non-whitespace value

        Tests that the given tag has at least one value and that its first value
        contains non-whitespace characters.

        Adds a string to the problems list if validation fails.

        Args:
            tag (str): Tag name to check
        """
        if not self.has_items(tag):
            self.problems.append('Missing {}'.format(tag))
        elif not self.get_first(tag).strip():
            self.problems.append('Empty {}'.format(tag))

    def validate_tag_appears_once(self, tag: str):
        """
        Validate that a tag has a single value

        Adds a string to the problems list if validation fails.

        Args:
            tag (str): Tag name to check
        """
        if self.has_items(tag, 2):
            self.problems.append("Multiple {}s: {}".format(tag, ', '.join(self.tags[tag])))

    def validate(self, strict=False):
        """
        Validate the presence of a few required elements: description and type.

        Validations:
            * Description have non-whitespace text
            * Type must have a non-whitespace value
            * (strict) Type cannot have more than one value
            * (strict) Type must be for our class
            * Name must have a non-whitespace value
            * (strict) Tags not in KNOWN_TAGS cannot be present

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this Character has no validation problems, false if not.
        """

        self.problems = []
        if not self.description.strip():
            self.problems.append("Missing description")

        self.validate_tag_present_and_filled('type')

        if strict:
            self.validate_tag_appears_once('type')
            right_class = npc.character.character_klass_from_type(self.type_key).__name__
            current_class = self.__class__.__name__
            if right_class != current_class:
                self.problems.append("Incorrect type '{}' for class '{}': implies class '{}'".format(self.type_key, current_class, right_class))

        self.validate_tag_present_and_filled('name')

        if strict:
            unknown_tags = [tag for tag in set(self.tags.keys()) - set(self.KNOWN_TAGS)]
            if unknown_tags:
                self.problems.append("Unrecognized tags: {}".format(', '.join(unknown_tags)))

        self.type_validations(strict=strict)

        return self.valid

    def type_validations(self, strict=False):
        """
        Validate additional elements based on type

        Subclasses should implement this method as needed, calling the existing
        validate_* methods and/or adding error messages to self.problems.

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            None
        """
        pass

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

        return len(self.tags.get(key, [])) >= threshold

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
        new_char.path = self.path
        for attr, values in self.tags.items():
            if attr == 'rank':
                for group, ranks in values.items():
                    for item in ranks:
                        new_char.append_rank(group, func(item))
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
            lines.extend(["@{} {}".format(attrname, val) for val in self.tags.get(attrname, [])])

        def buffered(attrname, fn):
            """Insert a newline before running fn, but only if attrname exists"""
            if attrname in self.tags:
                lines.append("")
                fn(attrname)

        def add_flag(attrname):
            """Add a bare tag, with no value, as long as attrname exists"""
            if attrname in self.tags:
                lines.append("@{}".format(attrname))

        def tags_or_flag(attrname):
            """Add tags or a flag for attrname, whichever is more appropriate."""
            if attrname in self.tags:
                if self.has_items(attrname):
                    tags_for_all(attrname)
                else:
                    add_flag(attrname)

        add_flag('skip')

        first_name = self.get_first('name')
        if first_name and first_name not in self.path:
            lines.append("@realname {}".format(first_name))
        lines.extend(["@name {}".format(val) for val in self.get_remaining('name')])

        # get type line(s)
        lines.extend(self.type_header())

        tags_for_all('faketype')

        tags_for_all('title')
        tags_or_flag('foreign')
        tags_for_all('location')
        add_flag('wanderer')

        tags_for_all('freehold')

        for tagname in self.GROUP_TAGS:
            for groupname in self.tags[tagname]:
                lines.append("@{} {}".format(tagname, groupname))
                if groupname in self.tags['rank']:
                    lines.extend(["@rank {}".format(rank) for rank in self.tags['rank'][groupname]])

        buffered('dead', tags_or_flag)
        buffered('appearance', tags_for_all)
        buffered('mask', tags_for_all)
        buffered('mien', tags_for_all)

        tags_for_all('hide')
        tags_for_all('hidegroup')
        tags_for_all('hideranks')

        return self.description + "\n".join(lines)

    def type_header(self):
        """
        Create type-specific header lines

        This implementation creates a plain '@type' tag and should should be
        implemented by subclasses as needed.

        Returns:
            List of strings describing the type-specific tags for this
            character.
        """
        return ["@type {}".format(self.get_first('type'))]

    def dump(self):
        """
        Create a single dict that represents all the data for this character

        The generated dict is the tag data combined with the file path.

        Returns:
            Dict containing all data for this character
        """
        dump = self.tags
        dump['path'] = self.path
        return dump
