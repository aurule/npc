"""
Helper functions unique to the settings module
"""

from ..util import index_compare

def merge_settings_dicts(new_data: dict, orig: dict) -> dict:
    dest = dict(orig)

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
