from .type_class import *

def make_types(type_defs: dict) -> dict:
    """Make Type objects for every type in a dict

    Iterates types in the type_defs dict, creating a Type object for each one.

    Args:
        type_defs (dict): Dict of type definitions to use

    Returns:
        dict: Dict of Type objects
    """
    return { type_name: Type(type_name, type_def) for (type_name, type_def) in type_defs.items() }
