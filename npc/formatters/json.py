import json
from datetime import datetime
from .. import commands

def dump(characters, f, include_metadata=False, metadata_extra={}, **kwargs):
    """
    Dump a json representation of all character data

    Internally, it adds the keys in meta if present and then calls `json.dump`.

    Args:
        characters (list): Character dicts to dump
        f (stream): Output stream to receive the json output
        include_metadata (bool): Whether to insert metadata keys
        metadata_extra (dict): Additional metadata keys. Ignored unless include_metadata is True.

    Returns:
        A commands.Result object. Openable will not be set.
    """
    if include_metadata:
        base_meta = {
            'meta': True,
            'title': 'NPC Listing',
            'created': datetime.now().isoformat()
        }
        meta = {**base_meta, **metadata_extra}
        characters = [meta] + characters

    try:
        json.dump(characters, f)
    except Exception as e:
        return commands.Result(False, errmsg=e, errcode=9)
    return commands.Result(True)
