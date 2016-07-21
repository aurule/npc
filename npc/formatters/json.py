"""
Formatter for creating json exports of a set of characters.

Has a single entry point `dump` which mostly just inserts metadata and calls
`json.dump`.
"""

import json
from datetime import datetime
from .. import util

def dump(characters, outstream, *, include_metadata=False, metadata_extra=None):
    """
    Dump a json representation of all character data

    Internally, it adds the keys in meta if present and then calls `json.dump`.

    Args:
        characters (list): Character dicts to dump
        outstream (stream): Output stream to receive the json output
            include_metadata (bool): Whether to insert a metadata object. The
            metadata object will always include a title and creation date, along
            with the key `"meta": true` to distinguish it from character data.
        metadata_extra (dict): Additional metadata keys. Ignored unless
            include_metadata is True. The keys 'meta', 'title', and 'created'
            will overwrite the generated values for those keys.

    Returns:
        A util.Result object. Openable will not be set.
    """
    if not metadata_extra:
        metadata_extra = {}

    if include_metadata:
        base_meta = {
            'meta': True,
            'created': datetime.now().isoformat()
        }
        meta = {**base_meta, **metadata_extra}
        characters = [meta] + characters

    try:
        json.dump(characters, outstream)
    except TypeError as err:
        return util.Result(False, errmsg=err, errcode=9)
    return util.Result(True)
