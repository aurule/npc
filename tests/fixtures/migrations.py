from pathlib import Path

from npc.settings import Settings
from npc.settings.migrations.settings_migration import SettingsMigration
from npc.settings.migrations.migration_message import MigrationMessage

class FakeMigration(SettingsMigration):
    """No-op migration for testing the SettingsMigration class
    """
    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()
        self.sequence = 10

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return self._sequence

    @sequence.setter
    def sequence(self, val: int):
        self._sequence = val

class MockMigration(SettingsMigration):
    """Configurable migration for testing SettingsMigrator class

    This migration is designed to have unique should_apply criteria that only
    allow it to operate on the fake "test" settings file key, which should
    never exist outside of a test.

    Set the key and value properties of the created migration object to set
    the outcome of applying the migration.
    """
    def __init__(self, settings: Settings):
        self.settings = settings
        self.key = "npc.tested"
        self.value = True

    def should_apply(self, file_key: str) -> bool:
        return file_key == "test"

    def config_dir_path(self, file_key: str) -> Path:
        # alternatie implementation to always get the key's saved file path
        return self.path_for_key(file_key)

    def migrate(self, file_key: str) -> list[MigrationMessage]:
        messages = []
        data = self.load_settings(file_key)
        data.set(self.key, self.value)
        messages.append(
            MigrationMessage(
                f"Set '{self.key}' to '{self.value}'",
                file=self.path_for_key(file_key),
                key=self.key))
        self.write_settings(file_key, data)
        return messages

    @property
    def sequence(self) -> int:
        return 20
