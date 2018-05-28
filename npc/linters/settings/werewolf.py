"""
Lint loaded werewolf settings
"""

from .settings_linter import SettingsLinter

def lint(prefs):
    """
    Check correctness of werewolf-specific settings.

    Args:
        prefs (Settings): Settings object to check

    Returns:
        A list of string error messages, or an empty list if no errors were
        found.
    """

    linter = WerewolfSettingsLinter(prefs)
    return linter.lint()

class WerewolfSettingsLinter(SettingsLinter):
    def lint(self):
        """
        Lint the given prefs

        Checks done:
        * Tribe names must not be shared between pure and moon lists.

        Args:
            prefs (Settings): Settings object to lint

        Returns:
            A list of strings representing errors.
        """
        self.check_shared_tribes()

        if not self.valid:
            self.errors.insert(0, 'Werewolf settings are not correct:')
        return self.errors

    def check_shared_tribes(self):
        moon = set(self.prefs.get('werewolf.tribes.moon', {}))
        pure = set(self.prefs.get('werewolf.tribes.pure', {}))

        if not moon.isdisjoint(pure):
            with self.error_section('Pure and non-pure tribes must be unique. Shared tribes:'):
                self.add_errors(moon.intersection(pure))
