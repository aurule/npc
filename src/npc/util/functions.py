"""
Shared helper functions
"""

import yaml
import subprocess
from click import launch
from pathlib import Path

from . import env
from .errors import ParseError, SchemaError

import logging
logger = logging.getLogger(__name__)

def parse_yaml(filename: Path):
    """Parse a YAML file

    Args:
        filename (Path): Path of the file to load

    Returns:
        List or dict from `yaml.safe_load()`
    """
    with open(filename, 'r') as f:
        try:
            return yaml.safe_load(f)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as err:
            nicestr = "Bad syntax in '{0}' line {2} column {3}: {1}"
            nicemsg = nicestr.format(filename, err.problem, err.problem_mark.line, err.problem_mark.column)
            raise ParseError(nicemsg, filename, err.problem_mark.line, err.problem_mark.column)

def index_compare(target_list: list, filter: callable) -> int:
    """Get the index of the first item in a list for which the filter returns true
    
    Uses callable to test every element of target_list. The first matching element has its index returned. If 
    none match, returns -1.
    
    Args:
        target_list (list): List to search
        filter (callable): Function to use to test each element. Must accept a single value.
    
    Returns:
        int: The index of the first element which matches the filter function, or -1 if none match
    """
    for index, value in enumerate(target_list):
        if filter(value):
            return index

    return -1

def prepend_namespace(data: any, namespace: str = None) -> dict:
    """Put data inside a nested dict

    Puts data inside one or more dicts as specified by namespace.
    For example:
        prepend_namespace("hello", "npc.greeting.first_time")
    returns:
        {"npc": {"greeting": {"first_time": "hello"}}}

    Args:
        data (any): Data to insert into a dict
        namespace (str): Key in dotted format for the namespace (default: `None`)

    Returns:
        dict: Nested dict using the namespace keys, containing data within the last key
    """
    if namespace is None or namespace == "":
        return dict(data)

    return_data: dict = {}

    key_parts: list = namespace.split('.')
    curr_dict: dict = return_data
    for i in range(0, len(key_parts) - 1):
        curr_dict[key_parts[i]] = {}
        curr_dict = curr_dict[key_parts[i]]
    curr_dict[key_parts[-1]] = data

    return return_data

def merge_data_dicts(new_data: dict, orig: dict) -> dict:
    """Merge one dictionary into another, and return the result

    This method does not modify the original dict.

    Add the keys in new_data to the orig dict. The logic for this merge is:
    1. If a key does not exist in orig, add it
    2. If orig[key] and new_data[key] are dicts, recurse
    3. Overwrite orig[key] with new_data[key]

    If orig[key] and new_data[key] have different types, npc.errors.SchemaError is raised.

    Args:
        new_data (dict): Dict to merge into orig
        orig (dict): Dict to receive new or updated keys

    Returns:
        dict: Result of the merge

    Raises:
        errors: npc.errors.SchemaError when the target key expects a dict or list, but receives something else
                in new_data
    """
    dest: dict = dict(orig)

    for key, val in new_data.items():
        if key not in dest:
            dest[key] = val
            continue

        if not isinstance(val, type(dest[key])):
            raise SchemaError("Expected {0} for '{1}', found {2}".format(type(dest[key]), key, type(val)))

        if isinstance(dest[key], dict):
            dest[key] = merge_data_dicts(val, dest[key])
        else:
            dest[key] = val

    return dest

def merge_data_lists(new_list: list, orig: list) -> list:
    """Merge two lists

    This method does not modify the original list.

    Add the values in new_list to the orig list. Values which are already present in orig are skipped.

    Args:
        new_list (list): List to merge into orig
        orig (list): List to receive new or updated keys

    Returns:
        list: Result of the merge
    """
    dest: list = list(orig)

    for val in new_list:
        if val not in dest:
            dest.append(val)

    return dest

def edit_files(files: list[Path], settings = None, *, debug: bool = False):
    """Edit one or more files

    If settings has a npc.editor key, that program is invoked for each file. Otherwise, click.launch is used
    to open each target file in the system's default program.

    Args:
        files (Tuple[list[Path]]): List of files to open
        settings (Settings): Settings file to use for getting the editor. If not supplied, a default settings
            object is created. (default: `None`)
        debug (bool): Whether to return debugging statements instead of invoking the editor (default: `False`)
    """
    from ..settings import Settings

    if settings is None:
        settings = Settings()

    opened: list = []

    for file_path in files:
        try:
            opened.append(run_editor(file_path, settings.get("npc.editor"), debug = debug))
        except FileNotFoundError:
            logger.error("Cannot open file. Check that your npc.editor setting is an absolute path or in your session PATH.")
            opened.append(f"Cannot open file {file_path}")

    return opened

def run_editor(file_path: Path, editor: str = None, *, debug: bool = False):
    """Open a file

    Args:
        file_path (Path): Path of the file to open
        editor (str): Name of the editor to use. Falls back on system behavior. (default: `None`)
        debug (bool): Whether to return debugging statements instead of invoking the editor (default: `False`)

    Returns:
        [str|bool]: Normally returns True once the editor is invoked. In debug mode, returns a string
        describing the action that would have been taken.

    Raises:
        FileNotFoundError: If the file does not exist, this error from the system is re-raised. Never raised
        in debug mode.
    """
    if env.testing():
        debug = True

    try:
        if editor:
            if debug:
                return f"Running {editor} with {file_path}"
            subprocess.run(args=[editor, file_path])
            return True
        else:
            if debug:
                return f"Launching {file_path}"
            launch(str(file_path))
            return True
    except FileNotFoundError as e:
        raise e

def arg_or_default(var, default) -> any:
    """Use var if defined, or default if not

    This small helper is meant to reduce the boilerplate for functions which accept optional arguments.
    When a function has something like argname=None, you can write:

        self.thing = arg_or_default(argname, default_value)

    Instead of

        if argname:
            self.thing = argname
        else:
            self.thing = default_value

    Args:
        var (any): The value to use if it is not falsey
        default (any): The value to return if var is falsey

    Returns:
        any: Var if that is truthy, otherwise default
    """
    if var:
        return var
    return default

def prune_empty_dirs(root_path: Path):
    """Remove all empty directories within a given root

    All empty directories are deleted. If this causes a parent dir to become empty, it is then also
    deleted. The root dir is never deleted.

    Args:
        root_path (Path): Directory whose descendents will be pruned
    """
    all_dirs = [dirpath for dirpath in root_path.rglob("*/")]
    for dirpath in reversed(all_dirs):
        try:
            dirpath.rmdir()
        except OSError as e:
            continue
