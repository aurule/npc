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

def test_gets_saved_version():
    migration = FakeMigration()
    key = "test"
    version = "1.2.3"
    migration.settings.versions[key] = version

    result = migration.version_for_key(key)

    assert str(result) == version

def test_returns_default_on_missing_key():
    migration = FakeMigration()
    key = "test"

    result = migration.version_for_key(key)

    assert str(result) == SettingsMigration.DEFAULT_VERSION

def test_returns_default_on_unusable_version():
    migration = FakeMigration()
    key = "test"
    version = "oh no my bones"
    migration.settings.versions[key] = version

    result = migration.version_for_key(key)

    assert str(result) == SettingsMigration.DEFAULT_VERSION
