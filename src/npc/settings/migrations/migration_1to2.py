from packaging.version import Version, parse, InvalidVersion

from .settings_migration import SettingsMigration
from npc.util import DataStore
from npc.util.legacy import load_json

import logging
logger = logging.getLogger(__name__)

class Migration1to2(SettingsMigration):

    MINIMUM_VERSION = "2.0.0"

    @property
    def sequence(self) -> int:
        """This migration is always first

        Returns:
            int: The sequence number of the SettingsMigration
        """
        return 0

    def should_apply(self, file_key: str) -> bool:
        """Whether this SettingsMigration should run on the given settings file

        This migration always runs when the detected settings version is below 2.0.0.

        Args:
            file_key (str): Key of the settings file to check

        Returns:
            bool: True if this SettingsMigration should be run on the given file, False if not
        """
        settings_version = self.version_for_key(file_key)
        minimum_version = Version(self.MINIMUM_VERSION)
        return settings_version < minimum_version

    def migrate(self, file_key: str) -> list:
        """Apply this SettingsMigration to a named settings file

        The file location is stored in settings.loaded_files. If the SettingsMigration succeeds, this method should
        always alter the file such that should_apply returns False in the future. This usually means updating
        the npc.version string to some minimum version.

        Args:
            file_key (str): Key of the settings file to modify
        """

        # Check for a settings.yaml file
        settings_path = self.path_for_key(file_key)
        if settings_path:
            legacy_data = self.load_yaml(file_key)
            if data.get("npc") or data.get("campaign"):
                data.set("npc.version", MINIMUM_VERSION)
                with settings_path.open('w', newline="\n"):
                    settings_path.write(data)
                return []

            return self.convert(file_key, data)

        # Check for settings.json and settings.yml files
        legacy_data = self.load_legacy(file_key)

        if not legacy_data:
            self.create_min_settings(file_key)
            return []

        return self.convert(file_key, legacy_data)

    def convert(self, file_key: str, legacy_data: DataStore):
        pass
        # gotta make a new settings file
        # move everything into /legacy
        # translate keys using legacy_keys.yaml
        # look for custom templates
        #   warn that they're incompatible and need to be converted
        # if paths.hierarchy is present, warn that it is replaced by campaign.subpath_components system
        #   Either convert automatically, or warn the user will need to replace it
        # look for old sheet template files and the types.key.sheet_template key
        #   warn that the files need to go in a new dir with new names, and that the settings key will be removed
        #   could move them automatically
        # if plot or session templates exist
        #   read in their contents and store in the settings file
        # if listing.sort_by is set
        #   translate the old constants to new constants
        # warn that some tags have changed, advise running the linter

    def load_legacy(self, file_key: str) -> DataStore:
        legacy_path = self.config_dir_path(file_key)
        json_path = legacy_path / "settings.json"
        yml_path = legacy_path / "settings.yml"
        store = DataStore()
        if json_path.exists():
            store.merge_data(load_json(json_path))
        elif yml_path.exists():
            store.merge_data(parse_yaml(json_path))
        else:
            return None

    def create_min_settings(self, file_key):
        new_settings = self.config_dir_path(file_key) / "settings.yaml"
        data = {
            "npc": {
                "version": self.MINIMUM_VERSION
            }
        }
        with new_settings.open('w', newline="\n"):
            new_settings.write(data)
