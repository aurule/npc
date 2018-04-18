"""
Linter for verifying werewolf character files

Checks for a number of problems that are specific to werewolf characters. The only
public entry point is the lint function.
"""

import re
from . import nwod

def lint(character, fix=False, *, strict=False, prefs=None):
    """
    Verify the more complex elements in a werewolf sheet.

    Checks for werewolf-specific problems within the rules blocks of the
    character sheet. The problems it checks for are as follows:

    1. Virtue and Vice are present (strict)
    2. Tribe is recognized
    3. Auspice is present if tribe is non-pure
    4. Auspice is not present if tribe is pure
    5. Auspice is recognized, if present

    Args:
        character (dict): Character data to lint
        fix (bool): Whether to automatically correct certain problems
        strict (bool): Whether to report non-critical errors and omissions
        prefs (Settings): Object storing the available auspices, tribes, and
            pure tribes.

    Returns:
        List of problem descriptions. If no problems were found, the list will
        be empty.
    """
    problems = []
    dirty = False

    # Ensure that tribe and auspice are correct
    problems.extend(lint_tribe(character, prefs))

    # If the character has no sheet, we cannot proceed
    if not character.has_path:
        problems.append('Missing path')
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

def lint_tribe(character, prefs):
    """
    Lint tribe and auspice issues
    """
    problems = []
    all_tribes = prefs.get('werewolf.tribes') + prefs.get('werewolf.pure')

    # Make sure tribe is present and recognized
    tribe = character.get_first('tribe')
    if not tribe:
        return problems
    if not tribe.lower() in all_tribes:
        problems.append("Unrecognized tribe '{}'".format(tribe))
        return problems

    # Get auspice
    auspice = character.get_first('auspice')

    # Pure don't have an auspice
    if tribe in prefs.get('werewolf.pure'):
        if auspice:
            problems.append('Auspice present, but werewolf is pure')

    # Other tribes must have an auspice and it must be recognized
    if tribe in prefs.get('werewolf.tribes'):
        if not auspice:
            problems.append('Missing auspice')
            return problems

        if auspice.lower() not in prefs.get('werewolf.auspices'):
            problems.append("Unrecognized auspice '{}'".format(auspice))

    return problems
