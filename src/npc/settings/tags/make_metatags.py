from .tag_spec_class import TagSpec, UndefinedTagSpec
from .deprecated_tag_spec_class import DeprecatedTagSpec
from .metatag_class import Metatag

def make_metatags(metatag_defs: dict) -> dict:
    """Make MetaTag objects for every metatag in a dict

    Args:
        metatag_defs (dict): Dict of metatag definitions to use

    Returns:
        dict: Dict of MetaTag objects
    """
    return {tag_name: Metatag(tag_name, tag_def) for tag_name, tag_def in metatag_defs.items()}
