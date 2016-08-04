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

from . import changeling
from .. import settings

def lint(character, fix=False, prefs=None):
    """
    Lint a character object

    Runs all available extra checks on a character.

    Args:
        character (Character): Character object to lint
        fix (bool): Whether to automatically correct certain problems
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
        problems.extend(changeling.lint(character, fix=fix, sk_data=prefs.get('changeling')))

    return problems
