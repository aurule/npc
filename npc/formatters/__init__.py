"""
Output formatters

The submodules in this package handle the logic for creating specially formatted
output for a few different commands. Each has one or more functions named after
the command they are designed for. Functions designed to work for the same
command share most of the same arguments, though optional arguments are
sometimes available.

The functions here can be used to easily get the appropriate formatting function
for a use case and output type.
"""

from . import markdown, json, html

BINARY_TYPES = ['html']
"""tuple: Format names that require a binary stream instead of a text stream"""

CANONICAL_FORMATS = {
    "md": "markdown",
    "markdown": "markdown",
    "htm": "html",
    "html": "html",
    "json": "json"
}
"""
dict: mapping of accepted format names and abbreviations to their canonical
format name keys
"""

def get_listing_formatter(format_name):
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
        return markdown.listing
    if format_name == 'html':
        return html.listing
    if format_name == 'json':
        return json.listing

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
    if format_name == 'markdown':
        return markdown.report
    if format_name == 'html':
        return html.report
    if format_name == 'json':
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
