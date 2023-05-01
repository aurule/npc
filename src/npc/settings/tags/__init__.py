from .tag_spec_class import TagSpec, UndefinedTagSpec
from .subtag_spec_class import SubTagSpec
from .deprecated_tag_spec_class import DeprecatedTagSpec

def make_tags(tag_defs: dict) -> dict:
    """Make TagSpec objects for every tag in a dict, including subtags

    Iterates the tags in the tag_defs dict, creating a TagSpec object for each one. Any subtags described are also
    created as top-level tags. It is up to the caller to handle adherance to any heirarchy.

    Args:
        tag_defs (dict): Dict of tag definitions to use

    Returns:
        dict: Dict of TagSpec objects
    """
    tags = {}

    for tag_name, tag_def in tag_defs.items():
        new_tag = TagSpec(tag_name, tag_def)
        tags[tag_name] = new_tag
        if tag_def.get("subtags"):
            make_subtags(tag_def.get("subtags"), new_tag, tags)

    return tags

def make_subtags(tag_defs: dict, parent_spec: TagSpec, all_specs: dict):
    """Create subtags from the passed tag_defs

    Creates any tags in tag_defs as subtags of parent_spec. Tags are all contained in all_specs, which is
    modified instead of returning a value.

    Args:
        tag_defs (dict): Tag definitions to parse
        parent_spec (TagSpec): Parent tag spec for all subtags
        all_specs (dict): Dict of tag specs that will be modified with new tags
    """
    for subtag_name, subtag_def in tag_defs.items():
        if subtag_name not in all_specs:
            all_specs[subtag_name] = SubTagSpec(subtag_name)
        all_specs[subtag_name].add_context(parent_spec.name, TagSpec(subtag_name, subtag_def))
        if subtag_def.get("subtags"):
            make_subtags(subtag_def.get("subtags"), all_specs[subtag_name], all_specs)
