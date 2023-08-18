from functools import cached_property
from pathlib import Path

from npc.settings import Settings

class SettingsMigrator:
    def __init__(self, settings: Settings):
        self.settings = Settings

    def needs_migration(self) -> list[str]:
        return [p for p in self.settings.loaded_paths.keys() if self.can_migrate(p)]
        # get settings file keys that need migration

    def can_migrate(self, file_key: str) -> bool:
        return any([m.should_apply(file_key) for m in self.migrations])
        # get if a key needs a migration

    def migrate(self):
        pass
        # apply all migrations to the settings object

    @cached_property
    def migrations() -> list[Migration]:
        """Get an instance of all known migration subclasses

        This simply gets a list of classes which subclass Migration and instantiates them.

        Returns:
            list[Migration]: List of Migration subclass objects
        """
        return [klass(self.settings) for klass in Migration.__subclasses__()].sort()
        # get objects for all migrations
