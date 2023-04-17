import logging

from .tag_class import Tag

class SubTag():
    """Represents a subtag

    Subtags are defined within a parent tag and cannot appear without a parent. Each subtag can have multiple
    parent tags and mean something different for each one. These different definitions are referred to as contexts.
    """
    def __init__(self, name: str):
        self.name: str = name
        self.contexts = {}

    def add_context(self, parent_key: str, props_obj: Tag):
        """Add a context to this subtag

        Adds a parent tag and the Tag definition this subtag should use when associated with that parent tag.

        Args:
            parent_key (str): Key of the parent tag
            props_obj (Tag): Tag object defining how this subtag should act when paired with the given parent
        """
        self.contexts[parent_key] = props_obj

    def in_context(self, parent_key: str) -> Tag:
        """Get the definition for this subtag in the given context

        Args:
            parent_key (str): Key of the parent tag

        Returns:
            Tag: Effective definition for this subtag in the context of the given parent
        """
        return self.contexts.get(parent_key)
