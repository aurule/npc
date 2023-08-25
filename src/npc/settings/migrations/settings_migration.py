from abc import ABC, abstractmethod
from packaging import version

from npc.settings import Settings

class SettingsMigration(ABC):
    """Core migration class

    Defines the interface and some helpers for settings migrations.
    """

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

    @abstractmethod
    @property
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
        if not issubclass(other, self.__class__):
            raise NotImplementedError

        return self.sequence < other.sequence

    def path_for_key(self, file_key: str) -> Path:
        return self.settings.loaded_paths.get(file_key)

    def version_for_key(self, file_key: str) -> version.Version:
        error_version = version.Version("0.0.0")
        version_str = self.settings.versions.get(file_key)

        if not version_str:
            # log that there's no version for file_key
            return error_version

        try:
            return version.parse(version_str)
        except version.InvalidVersion:
            # log that version_str for file_key is not a valid version number
            return error_version
