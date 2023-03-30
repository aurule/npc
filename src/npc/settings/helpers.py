"""
Helper functions unique to the settings module
"""

from ..util import index_compare

def merge_settings_dicts(new_data: dict, orig: dict) -> dict:
    """Merge one dictionary into another, and return the result

    This method does not modify the original dict.

    Add the keys in new_data to the orig dict. The logic for this merge is:
    1. If a key does not exist in orig, add it
    2. If orig[key] and new_data[key] are dicts, recurse
    3. If orig[key] and new_data[key] are lists, call merge_tags_lists to handle that logic
    4. Overwrite orig[key] with new_data[key]

    If orig[key] and new_data[key] have different types, npc.errors.SchemaError is raised.

    Args:
        new_data (dict): Dict to merge into orig
        orig (dict): Dict to receive new or updated keys

    Returns:
        dict: Result of the merge

    Raises:
        errors: npc.errors.SchemaError when the target key expects a dict or list, but receives something else
                in new_data
    """
    dest: dict = dict(orig)

    for key, val in new_data.items():
        if key not in dest:
            dest[key] = val
            continue

        if isinstance(dest[key], dict):
            if not isinstance(val, dict):
                raise errors.ParseError("Expected dict for '{0}', found {1}".format(key, type(val)))
            dest[key] = merge_settings_dicts(val, dest[key])
        elif isinstance(dest[key], list):
            if not isinstance(val, list):
                raise errors.ParseError("Expected list for '{0}', found {1}".format(key, type(val)))
            dest[key] = merge_tags_lists(val, dest[key])
        else:
            dest[key] = val

    return dest

def merge_tags_lists(new_tags: list, orig: list) -> list:
    dest: list = list(orig)

    for val in new_data:
        if val in dest:
            continue

        if isinstance(val, dict):
            key: int = index_compare(dest, lambda q: q.name == val.name)
            if key < 0:
                dest.push(val)
                continue
            dest[key] = merge_settings_dicts(val, dest[key])
        else:
            dest.push(val)

    return dest
