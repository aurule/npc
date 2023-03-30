"""
Shared helper functions
"""

import yaml
from pathlib import Path

from . import errors

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
            raise errors.ParseError(nicemsg, filename, err.problem_mark.line, err.problem_mark.column)

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
