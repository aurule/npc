"""
Helper functions shared between the other modules
"""

import re
import json
import sys
from os import getcwd, path
from subprocess import run

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
        r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    with open(filename) as json_file:
        content = ''.join(json_file.readlines())

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        # Return parsed json
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as err:
            nicestr = "Bad syntax in '{0}' line {2} column {3}: {1}"
            err.nicemsg = nicestr.format(filename, err.msg, err.lineno, err.colno)
            raise err
        except OSError as err:
            err.nicemsg = "Could not load '{0}': {1}".format(filename, err.strerror)
            raise err

def error(*args, **kwargs):
    """
    Print an error message to stderr.

    Args:
        Same as print(). The `file` param is prepopulated with sys.stderr.
    """
    print(*args, file=sys.stderr, **kwargs)

def flatten(thing):
    """
    Flatten a non-homogenous list

    Example:
        >>> flatten([1, 2, [3, [4, 5]], 6, [7, 8]])
        [1, 2, 3, 4, 5, 6, 7, 8]

    Args:
        thing (list): The list to flatten. Items can be lists or other types.

    Yields:
        Items from the list and any lists within it, as though condensed into a
            single, flat list.
    """
    for item in thing:
        if hasattr(item, '__iter__') and not isinstance(item, str):
            for flattened_item in flatten(item):
                yield flattened_item
        else:
            yield item

def merge_to_dict(target_dict: dict, key: str, value):
    """
    Merge a key and value into an existing dict

    Assumes that target_dict[key] exists and responds to `append`.

    Args:
        target_dict (dict): Dictionary to merge into
        key (str): Key to merge
        value (any):
    """
    if value is None:
        target_dict[key]
    elif hasattr(value, '__iter__') and not isinstance(value, str):
        target_dict[key] += value
    else:
        target_dict[key].append(value)

def find_campaign_root():
    """
    Determine the base campaign directory

    Walks up the directory tree until it finds the '.npc' campaign config
    directory, or hits the filesystem root. If the `.npc` directory is found,
    its parent is assumed to be the campaign's root directory. Otherwise, the
    current directory of the command invocation is used.

    Returns:
        Directory path to the campaign.
    """
    current_dir = getcwd()
    base = current_dir
    old_base = ''
    while not path.isdir(path.join(base, '.npc')):
        old_base = base
        base = path.abspath(path.join(base, path.pardir))
        if old_base == base:
            return current_dir
    return base

def open_files(*files, prefs=None):
    """
    Open a list of files with the configured editor

    Args:
        files (str): List of file paths to open
        prefs (Settings): Settings object to supply the editor name

    Returns:
        CompletedProcess object as per subprocess.run
    """
    return run(args=[prefs.get("editor"), *files])

class Singleton(type):
    """
    Metaclass for creating singleton classes.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class OutOfBoundsError(ValueError):
    """Raise when a function input is outside of permitted bounds"""

def serialize_args(*argnames, **full_args):
    serial_args = [full_args.pop(k) for k in argnames]
    return serial_args, full_args
