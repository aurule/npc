import npc
from npc.linters.settings.werewolf import WerewolfSettingsLinter

class TestLint:
    def test_prepends_generic_warning(self):
        prefs = npc.settings.Settings()
        linter = WerewolfSettingsLinter(prefs)

        linter.errors = ['hello']
        linter.lint()

        assert linter.errors[0] == 'Werewolf settings are not correct:'

class TestChecks:
    def test_check_shared_tribes(self):
        prefs = npc.settings.Settings()
        linter = WerewolfSettingsLinter(prefs)

        prefs.update_key('werewolf.tribes.moon', ['slow-aged', 'blue'])
        prefs.update_key('werewolf.tribes.pure', ['fast-aged', 'blue'])
        linter.check_shared_tribes()
        error_string = '\n'.join(linter.errors)

        assert 'Pure and non-pure tribes must be unique.' in error_string
        assert 'blue' in error_string
