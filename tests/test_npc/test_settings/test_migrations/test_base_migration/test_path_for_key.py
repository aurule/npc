import pytest

from npc.settings import Settings

from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self):
        self.settings = Settings()

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return 10

def test_gets_saved_path(tmp_path):
    migration = FakeMigration()
    key = "test"
    migration.settings.loaded_paths[key] = tmp_path

    result = migration.path_for_key(key)

    assert result == tmp_path

def test_returns_none_when_no_path():
    migration = FakeMigration()
    key = "test"

    result = migration.path_for_key(key)

    assert result is None
