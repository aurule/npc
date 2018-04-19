import npc
from npc.linters.settings.changeling import ChangelingSettingsLinter

class TestLint:
    def test_prepends_generic_warning(self):
        prefs = npc.settings.Settings()
        linter = ChangelingSettingsLinter(prefs)

        linter.errors = ['hello']
        linter.lint()

        assert linter.errors[0] == 'Changeling settings are not correct:'

class TestChecks:
    def test_check_seemings_have_blessings(self):
        prefs = npc.settings.Settings()
        linter = ChangelingSettingsLinter(prefs)

        prefs.update_key('changeling.seemings', ['fake'])
        linter.check_seemings_have_blessings()
        error_string = '\n'.join(linter.errors)

        assert 'Seemings must all have a blessing' in error_string
        assert 'fake' in error_string

    def test_check_seemings_have_curses(self):
        prefs = npc.settings.Settings()
        linter = ChangelingSettingsLinter(prefs)

        prefs.update_key('changeling.seemings', ['fake'])
        linter.check_seemings_have_curses()
        error_string = '\n'.join(linter.errors)

        assert 'Seemings must all have a curse' in error_string
        assert 'fake' in error_string

    def test_check_kiths_have_blessings(self):
        prefs = npc.settings.Settings()
        linter = ChangelingSettingsLinter(prefs)

        prefs.update_key('changeling.kiths.beast', ['fake'])
        linter.check_kiths_have_blessings()
        error_string = '\n'.join(linter.errors)

        assert 'Kiths must all have a blessing' in error_string
        assert 'fake' in error_string

    def test_check_kiths_have_one_seeming(self):
        prefs = npc.settings.Settings()
        linter = ChangelingSettingsLinter(prefs)

        prefs.update_key('changeling.kiths.beast', ['fake'])
        prefs.update_key('changeling.kiths.wizened', ['fake'])
        linter.check_kiths_have_one_seeming()
        error_string = '\n'.join(linter.errors)

        assert 'Kiths must belong to one seeming' in error_string
        assert 'fake' in error_string
