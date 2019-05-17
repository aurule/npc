"""
Formatter for creating json exports of a set of characters.

The functions in this module are very barebones and rely on json.dump to handle
the actual output. At most, they add some keys to the data first.
"""

import json
import npc
from npc.util import result

def listing(characters, outstream, *, metadata_format=False, metadata=None, **kwargs):
    """
    Dump a json representation of all character data

    Internally, it adds the keys in meta if present and then calls `json.dump`.

    Args:
        characters (list): Character dicts to dump
        outstream (stream): Output stream
        metadata_format (bool): Whether to insert a metadata object. The
            metadata object will always include a title and creation date, along
            with the key `"meta": true` to distinguish it from character data.
        metadata (dict): Additional metadata keys. Ignored unless
            metadata_format is True. The keys 'meta', 'title', and 'created'
            will overwrite the generated values for those keys.

    Returns:
        A util.Result object. Openable will not be set.
    """
    if not metadata:
        metadata = {}

    characters = [c.tags for c in characters]

    if metadata_format:
        meta = {'meta': True, **metadata}
        characters = [meta] + characters

    try:
        json.dump(characters, outstream)
    except TypeError as err:
        return result.Failure(errmsg=err)
    return result.Success()

def report(tables, outstream, **kwargs):
    """
    Write a json representation of one or more sets of table data

    Table data format:
    The tables arg is much more permissive for this formatter than for the other
    formatters. Since this formatter just dumps that arg as json, it can contain
    basically anything. For compatability, however, the following format should
    be followed:

    The tables arg should be a dictionary of collections.Counter objects indexed
    by the name of the tag whose data is stored in the Counter. The tag name
    will be titleized and used as the header for that column of the report.

    Args:
        tables (dict): One or more objects with table data
        outstream (stream): Output stream

    Returns:
        A util.Result object. Openable will not be set.
    """
    try:
        json.dump(tables, outstream)
    except TypeError as err:
        return result.Failure(errmsg=err)
    return result.Success()

