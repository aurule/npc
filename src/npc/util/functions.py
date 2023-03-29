"""
Shared helper functions
"""

import yaml
from . import errors

def parse_yaml(filename):
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

def index_compare(target_list: list, filter: callable) -> int:
    for index, value in enumerate(target_list):
        if filter(value):
            return index

    return -1
