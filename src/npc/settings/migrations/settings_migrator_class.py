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
        """Get whether a named settings file can be migrated

        If any migration class can run on the settings file from file_key, this
        will return true.

        Args:
            file_key (str): Key of the settings file to check

        Returns:
            bool: True if one or more migrations can run on the named settings file. False if not.
        """
        return any([m.should_apply(file_key) for m in self.migrations])

    def migrate(self, file_key: str) -> list[MigrationMessage]:
        """Apply the migrations for a given settings file

        All migrations that want to apply to file_key will be run in order of their sequence.

        Args:
            file_key (str): Key of the settings file to migrate

        Returns:
            list[MigrationMessage]: List of message objects that can be displayed to the user.
        """
        messages = []
        for migration in self.migrations_by_file_key().get(file_key, []):
            messages.extend(migration.migrate(file_key))
        return messages

    def migrate_all(self) -> list[MigrationMessage]:
        """Apply migrations for all possible settings files

        Each file_key with migrations that want to run wil have those migrations
        run in order of their sequence.

        Returns:
            list[MigrationMessage]: List of message objects that can be displayed to the user.
        """
        messages = []
        for file_key, file_migrations in self.migrations_by_file_key().items():
            for migration in file_migrations:
                messages.extend(migration.migrate(file_key))
        return messages

    def migrations_by_file_key(self) -> dict:
        """Get migration objects which want to apply to each known file_key

        Each file_key will appear as a key in the dict. Each value is a list of objects.

        Returns:
            dict: Dict of lists of migration objects keyed by the file_key they apply to.
        """
        return {key: sorted([
            m for m in self.migrations if m.should_apply(key)
        ]) for key in self.file_keys}

    @cached_property
    def migrations(self) -> list[SettingsMigration]:
        """Get an instance of all known migration subclasses

        This simply gets a list of classes which subclass Migration and instantiates them.

        Returns:
            list[Migration]: List of Migration subclass objects
        """
        return sorted([klass(self.settings) for klass in SettingsMigration.__subclasses__()])

    @property
    def file_keys(self) -> list[str]:
        """Get the available settings file_keys

        Only settings keys with a loaded path are considered. The "package" and "internal" keys always exist
        and refer to files that cannot be altered by migrations, so they are skipped.

        Returns:
            list[str]: List of settings file keys with an associated file.
        """
        return [k for k in self.settings.loaded_paths.keys() if (k not in ("package", "internal"))]
