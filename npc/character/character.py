import npc
from npc.util import OutOfBoundsError, flatten, merge_to_dict

from .tags import TagContainer

from collections import defaultdict

class Character:
    """
    Object to hold and access data for a single character

    Tag data is stored in a TagContainer object.
    """

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
                character's tags. If a value is a bare string, it will be
                converted to a list containing only that string.
            other_char (Character): Existing character object to copy. Tags from
                that object will be copied verbatim with no changes.
            path (pathlike): Path to the file this character object represents.
            **kwargs: Named arguments will be added verbatim to the new
                character's tags. Keys here will overwrite keys of the same name
                from the `attributes` arg. The values here are not altered at
                all.
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
        self.tags.add_tag('faketype', limit=1)
        self.tags.add_tag('title')
        self.tags.add_tag('appearance')
        self.tags.add_tag('location')
        self.tags.add_tag('race')
        self.tags.add_tag('age')
        self.tags.add_tag('employer')
        self.tags.add_flag('foreign')
        self.tags.add_flag('wanderer')
        self.tags.add_flag('skip')
        self.tags.add_flag('nolint')
        self.tags.add_flag('keep')
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

            if self.tags('nolint').present and not self.tags('skip').present:
                self.problems.append("Linting disabled, but character is visible in lists")

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
        header_tags = self.tags.present()

        # add realname tag if needed
        if 'name' in header_tags:
            first_name = header_tags('name').first_value()
            if first_name not in self.path:
                header_tags.add_tag('realname', first_name)
                header_tags['name'] = header_tags('name').remaining()

        # add compound tags as needed
        header_tags = self.add_compound_tags(header_tags).present()

        lines = [tag.to_header() for tag in header_tags.values()]
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

    def sanitize(self):
        """
        Hide and obfuscate this character for generating a listing

        Sanitize does these steps:
        1. Remove all hidden tag values
        2. Replace real type with false type if present
        3. Use a placeholder for unknown type

        This is a destructive operation which changes the character's data!
        """

        # Remove all hidden tag values
        self.tags.sanitize()

        # Replace real type with false type if present
        if self.tags('faketype').filled:
            self.tags['type'] = self.tags['faketype']

        # Use a placeholder for unknown type
        if not self.tags('type').filled:
            self.tags('type').append('Unknown')
