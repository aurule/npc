"""
Formatter for creating json exports of a set of characters.

Has a single function `dump` which mostly just inserts metadata and calls
`json.dump`.
"""

import json
from .. import util

def dump(characters, outstream, *, include_metadata=False, metadata=None, **kwargs):
    """
    Dump a json representation of all character data

    Internally, it adds the keys in meta if present and then calls `json.dump`.

    Args:
        characters (list): Character dicts to dump
        outstream (stream): Output stream
        include_metadata (bool): Whether to insert a metadata object. The
            metadata object will always include a title and creation date, along
            with the key `"meta": true` to distinguish it from character data.
        metadata (dict): Additional metadata keys. Ignored unless
            include_metadata is True. The keys 'meta', 'title', and 'created'
            will overwrite the generated values for those keys.

    Returns:
        A util.Result object. Openable will not be set.
    """
    if not metadata:
        metadata = {}

    if include_metadata:
        meta = {'meta': True, **metadata}
        characters = [meta] + characters

    try:
        json.dump(characters, outstream)
    except TypeError as err:
        return util.Result(False, errmsg=err, errcode=9)
    return util.Result(True)

def report(tables, outstream, **kwargs):
    """
    Write a json representation of one or more sets of table data

    Args:
        tables (dict): One or more objects with table data
        outstream (stream): Output stream

    Returns:
        A util.Result object. Openable will not be set.
    """
    try:
        json.dump(tables, outstream)
    except TypeError as err:
        return util.Result(False, errmsg=err, errcode=9)
    return util.Result(True)

