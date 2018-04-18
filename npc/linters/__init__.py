"""
Extra linters for verifying the correctness of certain character types

The validate method on Character objects does basic linting for every character
type, but some extra checks are possible for certain ones. The linters in this
package encapsulate that logic.

All linter packages have a single main entry point `lint` which accepts a
character information dict. Various keyword arguments are used for options and
supporting data.

If you just want to lint a character, call character.validate() and then
linters.lint(character). If you want to do special linting with custom options,
use a discrete linter function.
"""

from . import changeling, human, werewolf
from .. import settings

def lint(character, fix=False, prefs=None, strict=False):
    """
    Lint a character object

    Runs all available extra checks on a character.

    Args:
        character (Character): Character object to lint
        fix (bool): Whether to automatically correct certain problems
        strict (bool): Whether to report non-critical errors and omissions
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        List of problem description strings
    """
    if not prefs:
        prefs = settings.InternalSettings()

    problems = []
    all_types = [t.lower() for t in character['type']]

    if 'changeling' in all_types:
        problems.extend(
            changeling.lint(character,
                fix=fix,
                strict=strict,
                sk_data=prefs.get('changeling')))
    elif 'werewolf' in all_types:
        problems.extend(
            werewolf.lint(character, fix=fix, strict=strict, prefs=prefs))
    elif 'human' in all_types:
        problems.extend(
            human.lint(character, fix=fix, strict=strict))

    return problems
