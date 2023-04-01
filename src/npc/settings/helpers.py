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
            dest[key] = merge_settings_lists(val, dest[key])
        else:
            dest[key] = val

    return dest

def merge_settings_lists(new_list: list, orig: list) -> list:
    """Merge two lists

    This method does not modify the original list.

    Add the values in new_list to the orig list. Values which are already present in orig are skipped.

    Args:
        new_list (list): List to merge into orig
        orig (list): List to receive new or updated keys

    Returns:
        list: Result of the merge
    """
    dest: list = list(orig)

    for val in new_list:
        if val not in dest:
            dest.append(val)

    return dest

def prepend_namespace(data: any, namespace: str = None) -> dict:
    """Put data inside a nested dict
    
    Puts data inside one or more dicts as specified by namespace.
    For example:
        prepend_namespace("hello", "npc.greeting.first_time")
    returns:
        {"npc": {"greeting": {"first_time": "hello"}}}
    
    Args:
        data (any): Data to insert into a dict
        namespace (str): Key in dotted format for the namespace (default: `None`)
    
    Returns:
        dict: Nested dict using the namespace keys, containing data within the last key
    """     
    if namespace is None or namespace == "":
        return dict(data)

    return_data: dict = {}

    key_parts: list = namespace.split('.')
    curr_dict: dict = return_data
    for i in range(0, len(key_parts) - 1):
        curr_dict[key_parts[i]] = {}
        curr_dict = curr_dict[key_parts[i]]
    curr_dict[key_parts[-1]] = data

    return return_data
