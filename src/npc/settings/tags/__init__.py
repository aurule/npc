from .tag_spec_class import TagSpec, UndefinedTagSpec
from .subtag_spec_class import SubTagSpec
from .deprecated_tag_spec_class import DeprecatedTagSpec

def make_tags(tag_defs: dict, parent: str = None) -> dict:
    """Make TagSpec objects for every tag in a dict, including subtags

    Iterates the tags in the tag_defs dict, creating a TagSpec object for each one. Any subtags described are also
    created as top-level tags. It is up to the caller to handle adherance to any heirarchy.

    Args:
        tag_defs (dict): Dict of tag definitions to use
        parent (string): Name of the parent tag to assign to all created tags

    Returns:
        dict: Dict of TagSpec objects
    """
    tags = {}

    for tag_name, tag_def in tag_defs.items():
        new_tag = TagSpec(tag_name, tag_def)
        new_tag.parent = parent
        tags[tag_name] = new_tag
        for subtag_name, subtag_def in tag_def.get("subtags", {}).items():
            if subtag_name not in tags:
                tags[subtag_name] = SubTagSpec(subtag_name)
            tags[subtag_name].add_context(tag_name, TagSpec(subtag_name, subtag_def))

    return tags
