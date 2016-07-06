#!/usr/bin/env python3.5

import re
import json
import sys

def load_json(filename):
    """
    Parse a JSON file

    First remove all comments, then use the standard json package

    Comments look like :
        // ...
    or
        /*
        ...
        */

    Args:
        filename (str): Path of the file to load

    Returns:
        List or dict from `json.loads()`
    """
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    with open(filename) as f:
        content = ''.join(f.readlines())

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        # Return parsed json
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as e:
            e.nicemsg = "Bad syntax in '{0}' line {2} column {3}: {1}".format(filename, e.msg, e.lineno, e.colno)
            raise e
        except OSError as e:
            e.nicemsg = "Could not load '{0}': {1}".format(filename, e.msg)
            raise e

def error(*args, **kwargs):
    """
    Print an error message to stderr.

    Args:
        Same as print()
    """
    print(*args, file=sys.stderr, **kwargs)

class Singleton(type):
    """
    Metaclass for creating singleton classes.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
