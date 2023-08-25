from collections import defaultdict
from functools import cached_property
from pathlib import Path

from npc.settings import Settings

class SettingsMigrator:
    def __init__(self, settings: Settings):
        self.settings = Settings

    def migrations_by_file_key(self) -> dict:
        return {key: [
            m for m in self.migrations if m.should_apply(key)
        ].sorted() for key in self.file_keys}
        # get migration objects that need to be applied to each file

    def can_migrate(self, file_key: str) -> bool:
        return any([m.should_apply(file_key) for m in self.migrations])
        # get if a key needs a migration

    def migrate(self):
        for file_key, file_migrations in self.migrations_by_file_key().items():
            for migration in file_migrations:
                migration.migrate(file_key)
        # apply all migrations to the possible keys

    @cached_property
    def migrations(self) -> list[Migration]:
        """Get an instance of all known migration subclasses

        This simply gets a list of classes which subclass Migration and instantiates them.

        Returns:
            list[Migration]: List of Migration subclass objects
        """
        return [klass(self.settings) for klass in Migration.__subclasses__()].sort()
        # get objects for all migrations

    @property
    def file_keys(self) -> list[str]:
        return self.settings.loaded_paths.keys()
        # get available settings file keys
