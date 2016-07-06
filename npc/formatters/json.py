import json
from .. import commands

def dump(characters, out, meta=None):
    """
    Dump a json representation of all character data

    Internally, it adds the keys in meta if present and then calls `json.dump`.

    Args:
        characters (list): Character dicts to dump
        out (stream): Output stream to receive the json output
        meta (dict): Metadata keys to add to the character data

    Returns:
        A commands.Result object. Openable will not be set.
    """
    if meta:
        characters = [meta] + characters

    try:
        json.dump(characters, out)
    except Exception as e:
        return commands.Result(False, errmsg=e, errcode=9)
    return commands.Result(True)
