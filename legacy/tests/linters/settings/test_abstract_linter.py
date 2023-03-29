import npc
from npc.linters.settings import SettingsLinter

class TestValid:
    def test_not_valid_with_errors(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        linter.errors = ['hello', 'goodbye']

        assert not linter.valid

    def test_is_valid_with_no_errors(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        linter.errors = []

        assert linter.valid

class TestAddError:
    def test_inserts_prefix(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        linter.error_prefix = '*'
        linter.add_error('hello')

        assert '* hello' in linter.errors

class TestAddErrors:
    def test_inserts_all_messages(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        addme = ['hello', 'goodbye']
        linter.add_errors(addme)

        assert linter.errors == ['* hello', '* goodbye']

class TestErrorSection:
    def test_changes_prefix(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        old_prefix = linter.error_prefix
        with linter.error_section('section'):
            assert old_prefix != linter.error_prefix

    def test_resets_prefix(self):
        prefs = npc.settings.Settings()
        linter = SettingsLinter(prefs)

        old_prefix = linter.error_prefix
        with linter.error_section('section'):
            pass
        assert old_prefix == linter.error_prefix
