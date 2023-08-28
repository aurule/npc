from abc import ABC, abstractmethod
from packaging import version
from pathlib import Path

from npc.settings import Settings

import logging
logger = logging.getLogger(__name__)

class SettingsMigration(ABC):
    """Core migration class

    Defines the interface and some helpers for settings migrations.
    """

    DEFAULT_VERSION = "0.0.0"

    def __init__(self, settings: Settings):
        self.settings = settings


    @abstractmethod
    def should_apply(self, file_key: str) -> bool:
        """Whether this SettingsMigration should run on the given settings file

        This will often involve using packaging.version to compare version numbers from settings.versions.

        Args:
            file_key (str): Key of the settings file to check

        Returns:
            bool: True if this SettingsMigration should be run on the given file, False if not
        """

    @abstractmethod
    def migrate(self, file_key: str):
        """Apply this SettingsMigration to a named settings file

        The file location is stored in settings.loaded_files. If the SettingsMigration succeeds, this method should
        always alter the file such that should_apply returns False in the future. This usually means updating
        the npc.version string to some minimum version.

        Args:
            file_key (str): Key of the settings file to modify
        """

    @property
    @abstractmethod
    def sequence(self) -> int:
        """Get the SettingsMigration's sequence number

        Running migrations in order prevents needing to try each SettingsMigration multiple times. The sequence number
        should be a power of 10 in most cases, to leave room for errors. If you're absolutely certain that
        two migrations will not interact, they can have the same sequence number. In that case, the order
        they run in is indeterminate.

        Returns:
            int: The sequence number of the SettingsMigration
        """

    def __lt__(self, other) -> bool:
        """Compare against another SettingsMigration

        This is primarily for sorting a list of SettingsMigration objects. A SettingsMigration is considered less than another
        when its sequence number is lower than the other's.

        Args:
            other (SettingsMigration): The SettingsMigration to compare against

        Returns:
            bool: True if our sequence is less than other.sequence, False if not

        Raises:
            NotImplementedError: Migrations cannot be compared against any other type
        """
        if not issubclass(other.__class__, self.__class__):
            raise NotImplementedError

        return self.sequence < other.sequence

    def path_for_key(self, file_key: str) -> Path:
        """Get the file path associated with the given settings file key

        This is a simple delegation helper to make migration code easier to write.

        Args:
            file_key (str): Key of the settings file to fetch

        Returns:
            Path: Path to the settings file matching the key, or None if the key is not found
        """
        return self.settings.loaded_paths.get(file_key)

    def version_for_key(self, file_key: str) -> version.Version:
        """Get a Version object for the saved version for the given key

        When a version is present for file_key, it gets parsed into a Version object and returned. When it
        isn't set -- or cannot be parsed -- a Version object using DEFAULT_VERSION is returned instead.

        Args:
            file_key (str): Key of the settings file whose version to fetch

        Returns:
            version.Version: Version object with the key's associated version, or DEFAULT_VERSION if missing
                or unusable.
        """
        error_version = version.Version(self.DEFAULT_VERSION)
        version_str = self.settings.versions.get(file_key)

        if not version_str:
            logger.debug(f"No version for {file_key}")
            return error_version

        try:
            return version.parse(version_str)
        except version.InvalidVersion:
            logger.debug(f"Unusable version '{version_str}' for {file_key}")
            return error_version
