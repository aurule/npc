"""
Linters for verifying the correctness of a Settings object
"""

from . import changeling, werewolf

def lint(prefs):
    """
    Lint a character object

    Runs all available extra checks on a character.

    Args:
        prefs (Settings): Settings object to lint

    Returns:
        List of problem description strings
    """
    problems = []

    problems.extend(changeling.lint(prefs))
    problems.extend(werewolf.lint(prefs))

    return problems
