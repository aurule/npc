from collections import defaultdict
from functools import cached_property
from pathlib import Path

from npc.settings import Settings
from .migration_message import MigrationMessage
from .settings_migration import SettingsMigration

class SettingsMigrator:
    def __init__(self, settings: Settings):
        self.settings = settings

    def can_migrate(self, file_key: str) -> bool:
        return any([m.should_apply(file_key) for m in self.migrations])
        # get if a key needs a migration

    def migrate(self, file_key: str) -> list[MigrationMessage]:
        messages = []

        for migration in self.migrations_by_file_key().get(file_key, []):
            messages.extend(migration.migrate(file_key))

        return messages
        # apply all migrations for the given key

    def migrate_all(self) -> list[MigrationMessage]:
        messages = []
        for file_key, file_migrations in self.migrations_by_file_key().items():
            for migration in file_migrations:
                messages.extend(migration.migrate(file_key))
        return messages
        # apply all migrations to the possible keys

    def migrations_by_file_key(self) -> dict:
        return {key: sorted([
            m for m in self.migrations if m.should_apply(key)
        ]) for key in self.file_keys}
        # get migration objects that need to be applied to each file

    @cached_property
    def migrations(self) -> list[SettingsMigration]:
        """Get an instance of all known migration subclasses

        This simply gets a list of classes which subclass Migration and instantiates them.

        Returns:
            list[Migration]: List of Migration subclass objects
        """
        return sorted([klass(self.settings) for klass in SettingsMigration.__subclasses__()])
        # get objects for all migrations

    @property
    def file_keys(self) -> list[str]:
        return [k for k in self.settings.loaded_paths.keys() if (k not in ("package", "internal"))]
        # get available settings file keys
