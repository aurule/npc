import npc
from npc.util import OutOfBoundsError, flatten, merge_to_dict

from .tags import TagContainer

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

        self.path = path
        self.tags = TagContainer()
        self.tags.add_tag('type', required=True, limit=1)
        self.tags.add_tag('name', required=True)
        self.tags.add_tag('faketype')
        self.tags.add_tag('title')
        self.tags.add_tag('appearance')
        self.tags.add_tag('location')
        self.tags.add_flag('foreign')
        self.tags.add_flag('wanderer')
        self.tags.add_flag('skip')
        self.tags.add_flag('dead')
        self.tags.add_group('group')

        self._add_default_tags()

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

    def _add_default_tags(self):
        """
        Add additional type-specific tags
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
        if not self.tags('type').filled:
            return None

        return self.tags('type').first_value().lower()

    @property
    def foreign(self):
        """
        bool: Whether this character has data in its foreign or wanderer tags
        """
        return self.tags('foreign').filled or self.tags('wanderer').present

    @property
    def locations(self):
        """
        iter: Non-empty foreign and location names
        """
        return self.tags('foreign').filled_data + self.tags('location').filled_data

    @property
    def has_locations(self):
        """
        bool: Whether this character has non-empty location names
        """
        return len(list(self.locations)) >= 1

    def validate(self, strict=False):
        """
        Validate the presence of a few required elements: description and type.

        Validations:
            * (strict) Type must be for our class

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this Character has no validation problems, false if not.
        """

        self.problems = []

        # get tag errors
        self.tags.validate(strict=strict)
        self.problems.extend(self.tags.problems)

        if strict:
            right_class = npc.character.character_klass_from_type(self.type_key).__name__
            current_class = self.__class__.__name__
            if right_class != current_class:
                self.problems.append("Incorrect type '{}' for class '{}': implies class '{}'".format(self.type_key, current_class, right_class))

        self.type_validations(strict=strict)

        return self.valid

    def type_validations(self, strict=False):
        """
        Validate additional elements based on type

        Subclasses should implement this method as needed, calling the existing
        validate_* methods and adding error messages to self.problems.

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            None
        """
        pass

    def build_header(self):
        """
        Build a large string of tag data

        Returns:
            A string containing tags that when parsed will recreate the data in
            this character object.
        """
        filled_tags = self.tags.present()

        if 'name' in filled_tags:
            first_name = filled_tags('name').first_value()
            if first_name not in self.path:
                filled_tags.add_tag('realname', first_name)
                filled_tags['name'] = filled_tags('name').remaining()

        filled_tags = self.add_compound_tags(filled_tags).present()

        lines = [tag.to_header() for tag in filled_tags.values()]
        return "\n".join(lines)

    def add_compound_tags(self, tags: TagContainer):
        """
        Apply type-specific modifications to the filled tags

        This is meant to be used to create compound tags, like @changeling and
        @werewolf.

        Args:
            tags (TagContainer): Container of filled tags that can be modified

        Returns:
            TagContainer with its contents modified as needed
        """
        return tags

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
