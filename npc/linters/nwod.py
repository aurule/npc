"""
Shared linting functions for New World of Darkness characters

These linting functions are not complete linters. They provide common tests that
can be shared by other New World of Darkness character type linters.
"""

import re

VICE_REGEX = r'^\s+vice\s+(?P<vice>\w+)$'
VIRTUE_REGEX = r'^\s+virtue\s+(?P<virtue>\w+)$'

def lint_vice_virtue(character_data):
    """
    Check that the character sheet has a vice and virtue listed

    Usually run as an optional test, but that is left up to the caller.

    Args:
        character_data (string): Character sheet to check

    Returns:
        List of problem descriptions
    """
    problems = []

    virtue_re = re.compile(
        VIRTUE_REGEX,
        re.MULTILINE | re.IGNORECASE
    )
    vice_re = re.compile(
        VICE_REGEX,
        re.MULTILINE | re.IGNORECASE
    )

    if vice_re.search(character_data) is None:
        problems.append('Missing vice')
    if virtue_re.search(character_data) is None:
        problems.append('Missing virtue')

    return problems
