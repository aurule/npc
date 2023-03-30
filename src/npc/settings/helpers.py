"""
Helper functions unique to the settings module
"""

from ..util import index_compare

from npc.util.errors import SchemaError


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

        if not isinstance(val, type(dest[key])):
            raise SchemaError("Expected {0} for '{1}', found {2}".format(type(dest[key]), key, type(val)))

        if isinstance(dest[key], dict):
            dest[key] = merge_settings_dicts(val, dest[key])
        elif isinstance(dest[key], list):
            dest[key] = merge_tags_lists(val, dest[key])
        else:
            dest[key] = val

    return dest

def merge_tags_lists(new_tags: list, orig: list) -> list:
    """Merge two lists that may contain tag data

    This method does not modify the original list.

    Add the keys in new_tags to the orig list. The logic for this merge is:
    1. If the new value is a dict, assume it describes a tag.
        a. If an entry exists in orig with the same name as the new value, call merge_settings_dicts to update the existing tag entry
        b. If no such entry exists, push the new tag onto the list
    2. Otherwise, push the new value onto the list

    Args:
        new_tags (list): List to merge into orig
        orig (list): List to receive new or updated keys

    Returns:
        list: Result of the merge
    """
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
