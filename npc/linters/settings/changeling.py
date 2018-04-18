"""
Lint loaded changeling settings
"""

from npc.util import flatten
from .settings_linter import SettingsLinter

def lint(prefs):
    """
    Check correctness of changeling-specific settings.

    Args:
        prefs (Settings): Settings object to check

    Returns:
        A list of string error messages, or an empty list if no errors were
        found.
    """

    linter = ChangelingSettingsLinter(prefs)
    return linter.lint()

class ChangelingSettingsLinter(SettingsLinter):
    def lint(self):
        """
        Lint the given prefs

        Checks done:
        * Every seeming must have a blessing
        * Every seeming must have a curse
        * Every kith must have a blessing
        * Each kith appears in a single seeming

        Args:
            prefs (Settings): Settings object to lint

        Returns:
            A list of strings representing errors.
        """
        self.check_seemings_have_blessings()
        self.check_seemings_have_curses()
        self.check_kiths_have_blessings()
        self.check_kiths_have_one_seeming()

        if not self.clean:
            self.errors.insert(0, 'Changeling settings are not correct:')
        return self.errors

    def check_seemings_have_blessings(self):
        blessings = set(self.prefs.get('changeling.blessings', {}).keys())
        seemings = set(self.prefs.get('changeling.seemings', []))

        if not blessings.issuperset(seemings):
            with self.error_section('Seemings must all have a blessing. Seemings without a blessing:'):
                self.add_errors(seemings.difference(blessings))

    def check_seemings_have_curses(self):
        curses = set(self.prefs.get('changeling.curses', {}).keys())
        seemings = set(self.prefs.get('changeling.seemings', []))

        if not curses.issuperset(seemings):
            with self.error_section('Seemings must all have a curse. Seemings without a curse:'):
                self.add_errors(seemings.difference(curses))

    def check_kiths_have_blessings(self):
        blessings = set(self.prefs.get('changeling.blessings', {}).keys())
        kith_indexes = self.prefs.get('changeling.kiths', {})
        kiths = set(flatten(kith_indexes.values()))

        if not blessings.issuperset(kiths):
            with self.error_section('Kiths must all have a blessing. Kiths without a blessing:'):
                self.add_errors(kiths.difference(blessings))

    def check_kiths_have_one_seeming(self):
        kith_sets = [set(kith_group) for kith_group in self.prefs.get('changeling.kiths').values()]

        dupe_kiths = set()
        while kith_sets:
            test_set = kith_sets.pop()
            unique_kiths = test_set.difference(*kith_sets)
            if test_set != unique_kiths:
                dupe_kiths = dupe_kiths.union(test_set - unique_kiths)

        if dupe_kiths:
            with self.error_section('Kiths must belong to one seeming. Kiths with multiple seemings:'):
                self.add_errors(dupe_kiths)
