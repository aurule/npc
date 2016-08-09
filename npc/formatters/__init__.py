"""
Character listing formatters

These modules encapsulate the logic needed to create a character listing in
various formats. Each module has a single `dump` entry point which accepts, at
minimum, the characters to list and where to put them. Other args are available
in each linter.
"""

from . import markdown, json, html

BINARY_TYPES = ('html')
"""tuple: Format names that require a binary stream instead of a text stream"""

CANONICAL_FORMATS = {
    "md": "markdown",
    "markdown": "markdown",
    "htm": "html",
    "html": "html",
    "json": "json"
}
"""dict: mapping of accepted format names and abbreviations and their canonical format name keys"""

def get_list_formatter(format_name):
    """
    Get the correct npc listing output function for a named format

    Args:
        format_name (str): Name of the desired format

    Returns:
        A formatting output function if the format is recognized, or None if it
        is not.
    """
    format_name = get_canonical_format_name(format_name)
    if format_name == 'markdown':
        return markdown.dump
    elif format_name == 'html':
        return html.dump
    elif format_name == 'json':
        return json.dump

    return None

def get_report_formatter(format_name):
    """
    Get the correct report table output function for a named format

    Args:
        format_name (str): Name of the desired format

    Returns:
        A formatting output function if the format is recognized, or None if it
        is not.
    """
    format_name = get_canonical_format_name(format_name)
    if format_name == 'html':
        return html.report
    elif format_name == 'json':
        return json.report

    return None

def get_canonical_format_name(format_name):
    """
    Get the canonical format name for a possible abbreviation

    Args:
        format_name (str): Format name or abbreviation

    Returns:
        The canonical name from CANONICAL_FORMATS, or None if the format is
        not recognized.
    """
    try:
        return CANONICAL_FORMATS[format_name.lower()]
    except KeyError:
        return None
