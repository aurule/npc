"""
Helper functions shared between the other modules
"""

import re
import json
import sys
import subprocess
import yaml
from . import errors
from os import getcwd
from pathlib import Path

def load_settings(file_path):
    """
    Load a supported settings file

    Checks the file suffix of file_path and calls the appropriate loader. No
    special checking is done on the file's contents.

    Args:
        file_path (Path): Path to the settings file to load

    Raises:
        FormatError when the suffix is not recognized
    """
    if file_path.suffix == '.yaml':
        return load_yaml(file_path)
    if file_path.suffix == '.json':
        return load_json(file_path)

    raise errors.FormatError("Unrecognized format for {}".format(file_path))

def load_yaml(filename):
    """
    Parse a YAML file

    Args:
        filename (str): Path of the file to load

    Returns:
        List or dict from `yaml.safe_load()`
    """
    with open(filename, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.parser.ParserError as err:
            nicestr = "Bad syntax in '{0}' line {2} column {3}: {1}"
            nicemsg = nicestr.format(filename, err.problem, err.problem_mark.line, err.problem_mark.column)
            raise errors.ParseError(nicemsg, filename, err.problem_mark.line, err.problem_mark.column)


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
        filename (str): Path of the file to load

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

    with open(filename) as json_file:
        content = ''.join(json_file.readlines())
        content = remove_comments(content) # Remove comments
        content = remove_trailing_commas(content) # Remove trailing commas

        # Return parsed json
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as err:
            nicestr = "Bad syntax in '{0}' line {2} column {3}: {1}"
            nicemsg = nicestr.format(filename, err.msg, err.lineno, err.colno)
            raise errors.ParseError(nicemsg, filename, err.lineno, err.colno)
        except OSError as err:
            err.strerror = "Could not load '{0}': {1}".format(filename, err.strerror)
            raise err

class PathEncoder(json.JSONEncoder):
    """
    Properly encode pathlib objects by casting to strings
    """
    def default(self, o):
        if isinstance(o, Path):
            return str(o)
        return json.JSONEncoder.default(self, o)

def print_err(*args, **kwargs):
    """
    Print a message to stderr.

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
    current_dir = Path.cwd()
    base = current_dir.resolve()
    old_base = Path('')
    while not base.joinpath('.npc').is_dir():
        old_base = base
        base = base.parent.resolve()
        if old_base.samefile(base):
            return current_dir
    return base

def open_files(*files, prefs=None):
    """
    Open a list of files with the configured editor

    Args:
        files (list[str]): List of file paths to open
        prefs (Settings): Settings object to supply the editor name

    Returns:
        CompletedProcess object as per subprocess.run
    """
    editor = determine_editor(sys.platform, prefs=prefs)

    for file_path in files:
        path_to_open = Path(file_path)
        subprocess.run(args=[editor, path_to_open])

def determine_editor(platform, prefs=None):
    """
    Figure out which editor to use for the system

    If an editor is set in settings, use that over all else. Otherwise, ask the
    OS to use its default program.

    Args:
        platform (str): Name of the current platform, as from sys.platform
        prefs (Settings): Settings object to supply the editor name

    Returns:
        String with the editor program to invoke
    """
    if prefs.get('editor'):
        return prefs.get('editor')
    elif 'linux' in platform:
        return 'xdg-open'
    elif 'darwin' in platform:
        return 'open'
    else:
        return 'start'

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
    """
    Split positional args from a set of keyword args

    Args:
        argnames (List[str]): Names of args to make positional
        full_args (dict): Keyword arguments dict

    Returns:
        Tuple of (positional args list, keyword args dict).
    """
    serial_args = [full_args.pop(k) for k in argnames]
    return serial_args, full_args

def listify_args(*argnames, **full_args):
    """
    Modify named keyword arguments to make them lists instead of strings.

    The lists are created by splitting each named value on commas, then
    stripping any extra white space. If the named arg is None, it is not
    modified.

    Args:
        argnames (List[str]): List of keyword argument names to modify
        full_args (dict): Keyword arguments dict

    Returns:
        New keyword arguments dict with the named arguments translated from
        strings into lists of strings.
    """
    for argname in argnames:
        if argname in full_args and full_args[argname] is not None:
            full_args[argname] = [s.strip() for s in full_args[argname].split(',') if s]
    return full_args
