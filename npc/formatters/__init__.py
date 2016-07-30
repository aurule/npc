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
