from .tag_class import Tag
from .deprecated_tag_class import DeprecatedTag

def make_tags(tag_defs: dict, parent: str = None) -> dict:
    """Make Tag objects for every tag in a dict, including subtags

    Iterates the tags in the tag_defs dict, creating a Tag object for each one. Any subtags described are also
    created as top-level tags. It is up to the caller to handle adherance to any heirarchy.

    Args:
        tag_defs (dict): Dict of tag definitions to use
        parent (string): Name of the parent tag to assign to all created tags

    Returns:
        dict: Dict of Tag objects
    """
    tags = {}

    for tag_name, tag_def in tag_defs.items():
        new_tag = Tag(tag_name, tag_def)
        new_tag.parent = parent
        tags[tag_name] = new_tag
        if "subtags" in tag_def:
            tags.update(make_tags(tag_def["subtags"], parent=tag_name))

    return tags
