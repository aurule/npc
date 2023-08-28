"""Helper functions for dealing with legacy campaigns

The way settings are stored and the location of helper files (templates, etc.) changed dramatically in
NPC 2.0. The helper functions here let us interact with older campaigns so that they can be migrated.
"""

import re
import json

def load_json(filename):
    """
    Parse a JSON-like file with non-standard syntax

    Two cleaning steps are done before parsing with the standard json package:
    1. Remove all comments
    2. Remove trailing commas from the last element of an object or list

    Comments look like :
        // ...
    or
        /*
        ...
        */

    Args:
        filename (Path): Path of the file to load

    Returns:
        List or dict from `json.loads()`
    """

    def remove_comments(json_like):
        """
        Removes C-style comments from *json_like* and returns the result.
        """
        comments_re = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        def replacer(match):
            s = match.group(0)
            if s[0] == '/': return ""
            return s
        return comments_re.sub(replacer, json_like)

    def remove_trailing_commas(json_like):
        """
        Removes trailing commas from *json_like* and returns the result.
        """
        trailing_object_commas_re = re.compile(r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
        trailing_array_commas_re = re.compile(r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
        # Fix objects {} first
        objects_fixed = trailing_object_commas_re.sub("}", json_like)
        # Now fix arrays/lists [] and return the result
        return trailing_array_commas_re.sub("]", objects_fixed)

    with filename.open() as json_file:
        content = ''.join(json_file.readlines())
        content = remove_comments(content) # Remove comments
        content = remove_trailing_commas(content) # Remove trailing commas

        # Return parsed json
        return json.loads(content)
