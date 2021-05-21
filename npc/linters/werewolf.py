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

    if character.type_key != 'werewolf':
        problems.append('Attempting to lint non-werewolf character using werewolf linter')
        return problems

    # Ensure that tribe and auspice are correct
    problems.extend(lint_tribe(character, prefs))

    # If the character has no sheet, we cannot proceed
    if not character.path:
        problems.append('Missing path')
        return problems

    # Load the sheet for deep linting
    with open(character.path, 'r') as char_file:
        data = char_file.read()

    # Check that they have a vice and a virtue
    if strict:
        problems.extend(nwod.lint_vice_virtue(data))

    if dirty and data:
        with open(character.path, 'w') as char_file:
            char_file.write(data)

    return problems

def lint_tribe(character, prefs):
    """
    Lint tribe and auspice issues
    """
    problems = []
    all_tribes = prefs.get('werewolf.tribes.moon') + prefs.get('werewolf.tribes.pure')

    # Make sure tribe is present and recognized
    if not character.tags('tribe').filled:
        return problems

    tribe = character.tags('tribe').first_value()
    tribe_key = tribe.lower()
    if not tribe_key in all_tribes:
        problems.append("Unrecognized tribe '{}'".format(tribe))

    # Get auspice
    if character.tags('auspice').filled:
        auspice = character.tags('auspice')[0]
        # Pure should not have an auspice
        if tribe_key in prefs.get('werewolf.tribes.pure'):
            problems.append('Auspice present, but werewolf is Pure')
        # regardless, auspice must be recognized
        if auspice.lower() not in prefs.get('werewolf.auspices'):
            problems.append("Unrecognized auspice '{}'".format(auspice))
    else:
        # Non-pure must have an auspice
        if tribe_key in prefs.get('werewolf.tribes.moon'):
            problems.append('Missing auspice')

    return problems
