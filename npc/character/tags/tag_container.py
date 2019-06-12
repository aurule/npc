from collections import UserDict
from copy import copy

from . import *

class TagContainer(UserDict):
    """
    Manages a coherent group of tags

    Instances are callable
    """
    def __init__(self):
        """
        Create a new tag container

        All tag containers start with a special DescriptionTag element for
        consistency.
        """
        super().__init__()
        self._add_taglike(DescriptionTag)
        self.problems = []

    def __call__(self, tag_name: str):
        """
        Get a tag by its name

        Tags which have already been defined will be returned as-is. Undefined
        tag names are assigned an UnknownTag object, which is then returned.

        Args:
            tag_name (str): Name of the tag to fetch

        Returns:
            A Tag or UnknownTag object
        """
        tag = self.data.get(tag_name)
        if tag is None:
            tag = UnknownTag(tag_name)
            self.append(tag)
        return tag

    def append(self, tag):
        """
        Add a tag to this container

        The tag will be indexed by its name

        Args:
            tag (Tag): A tag object
        """
        if tag.name in self.data:
            return

        self.data[tag.name] = tag

    def update(self, values: dict):
        """
        Update multiple tags using data from the values dict

        Args:
            values (dict): Dictionary of lists whose keys are tag names
        """
        for key, data in values.items():
            self(key).update(data)

    def all(self):
        """
        Iterate over the stored tag objects

        Returns:
            Iterator for the stored tag objects
        """
        return iter(self.data.values())

    def names(self):
        """
        Get a view of the tag names

        Returns:
            Dictionary view of the saved tag names
        """
        return self.data.keys()

    def present(self):
        """
        Create a new container with only the tags marked as present

        Returns:
            TagContainer object with only present tags
        """
        new_container = copy(self)
        new_container.data = {k: v for k, v in self.data.items() if v.present}
        return new_container

    def _add_taglike(self, klass, *args, **kwargs):
        """
        Internal method to create and append a new tag

        Args:
            klass (object): Tag class to create
            args, kwargs: Other arguments as appropriate for the tag to create
        """
        self.append(klass(*args, **kwargs))

    def add_tag(self, *args, **kwargs):
        """
        Add a new tag
        """
        self._add_taglike(Tag, *args, **kwargs)

    def add_flag(self, *args, **kwargs):
        """
        Add a new flag
        """
        self._add_taglike(Flag, *args, **kwargs)

    def add_group(self, *args, **kwargs):
        """
        Add a new group tag
        """
        self._add_taglike(GroupTag, *args, **kwargs)

    @property
    def valid(self):
        """
        bool: Whether this tag is internally valid

        This property is only meaningful after calling validate()
        """
        return len(self.problems) == 0

    def validate(self, strict: bool=False):
        """
        Validate all of the tags in this container

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this tag has no validation problems, false if not
        """
        self.problems = []

        for key, tag in self.data.items():
            tag.validate(strict=strict)
            self.problems.extend(tag.problems)
            if key != tag.name:
                self.problems.append("Tag '{}' has wrong key: '{}'".format(tag.name, key))

        return self.valid

    def remove_hidden(self):
        """
        Ask all tags to remove their hidden values

        Calls hide_values on each tag
        """
        for tag in self.values():
            tag.hide_values()
