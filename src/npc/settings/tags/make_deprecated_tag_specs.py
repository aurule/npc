from .deprecated_tag_spec_class import DeprecatedTagSpec

def make_deprecated_tag_specs(deprecated_tag_defs: dict) -> dict:
    """Make DeprecatedTagSpec objects for every deprecated tag in a dict

    Args:
        deprecated_tag_defs (dict): Dict of deprecated tag definitions to use

    Returns:
        dict: Dict of DeprecatedTagSpec objects
    """
    return {tag_name: DeprecatedTagSpec(tag_name, tag_def) for tag_name, tag_def in deprecated_tag_defs.items()}
