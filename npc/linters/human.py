"""
Linter for verifying human character files

Checks for a number of problems that are specific to human characters. The only
public entry point is the lint function.
"""

import re
from . import nwod
from .. import util

def lint(character, fix=False, *, strict=False):
    """
    Verify the more complex elements in a human sheet.

    Checks for human-specific problems within the rules blocks of the
    character sheet. The problems it checks for are as follows:

    1. Virtue and Vice are present (strict)

    Args:
        character (dict): Character data to lint
        fix (bool): Whether to automatically correct certain problems
        strict (bool): Whether to report non-critical errors and omissions

    Returns:
        List of problem descriptions. If no problems were found, the list will
        be empty.
    """
    problems = []
    dirty = False

    # If the character has no sheet, we're done
    if 'path' not in character:
        return problems

    # Load the sheet for deep linting
    with open(character['path'], 'r') as char_file:
        data = char_file.read()

    # Check that they have a vice and a virtue
    if strict:
        problems.extend(nwod.lint_vice_virtue(data))

    if dirty and data:
        with open(character['path'], 'w') as char_file:
            char_file.write(data)

    return problems
