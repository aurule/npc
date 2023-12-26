from .tag_spec_class import TagSpec

class SubTagSpec():
    """Represents a subtag

    Subtags are defined within a parent tag and cannot appear without a parent. Each subtag can have multiple
    parent tags and mean something different for each one. These different definitions are referred to as contexts.
    """
    def __init__(self, name: str):
        self.name: str      = name
        self.needs_context  = True
        self.contexts       = {}

    def __repr__(self) -> str:
        return f"SubTagSpec(name={self.name!r}, contexts={list(self.contexts.keys())})"

    def add_context(self, parent_key: str, props_obj: TagSpec):
        """Add a context to this subtag

        Adds a parent tag and the TagSpec definition this subtag should use when associated with that parent tag.

        Args:
            parent_key (str): Key of the parent tag
            props_obj (TagSpec): TagSpec object defining how this subtag should act when paired with the given parent
        """
        if props_obj.name != self.name:
            raise KeyError(f"Subtag {self.name} requires all context objs to have identical name")
        self.contexts[parent_key] = props_obj

    def in_context(self, parent_key: str, default=None) -> TagSpec:
        """Get the definition for this subtag in the given context

        Args:
            parent_key (str): Key of the parent tag
            default (any): Value to return if the named context does not exist

        Returns:
            TagSpec: Effective definition for this subtag in the context of the given parent
        """
        return self.contexts.get(parent_key, default)
