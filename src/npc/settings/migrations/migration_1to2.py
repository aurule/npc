from packaging.version import Version, parse, InvalidVersion
import yaml
from shutil import move

from .settings_migration import SettingsMigration
from npc.util import DataStore, parse_yaml
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
    def modern_format(self, file_key: str) -> bool:
        """Test whether a named settings file has a modern format

        The settings file is considered modern if it has the right filename and either the npc or campaign
        top-level key. Anything else is not a modern formatted settings file (and may not exist at all).

        Args:
            file_key (str): Key of the settings file to test

        Returns:
            bool: True if the file exists and has a modern format, False if not
        """
        if self.path_for_key(file_key):
            data = self.load_settings(file_key)
            return data.get("npc") or data.get("campaign")
        return False

    def load_legacy(self, file_key: str) -> DataStore:
        """Load a legacy settings file

        This tries to load a legacy json or yaml settings file. As in npc < 2.0, the json format is preferred
        and will be loaded in preference to a yaml file.

        Args:
            file_key (str): Key of the settings location to load legacy files from

        Returns:
            DataStore: DataStore containing the loaded legacy data, or empty if no legacy files were found
        """
        store = DataStore()

        legacy_path = self.config_dir_path(file_key)
        json_path = legacy_path / "settings.json"
        yml_path = legacy_path / "settings.yml"
        yaml_path = legacy_path / "settings.yaml"
        if json_path.exists():
            store.merge_data(load_json(json_path))
        elif yml_path.exists():
            store.merge_data(parse_yaml(yml_path))
        elif yaml_path.exists():
            store.merge_data(parse_yaml(yaml_path))

        return store

    def archive_legacy_files(self, file_key: str):
        """Move old files to a new legacy/ directory

        All existing files are moved to a new legacy/ directory under the file_key's path. If there are no
        files, the new directory is not created.

        Args:
            file_key (str): Key of the settings location to archive
        """
        settings_dir = self.config_dir_path(file_key)
        legacy_contents = list(settings_dir.glob("*"))
        if not legacy_contents:
            return

        legacy_dir = settings_dir.joinpath("legacy").mkdir(exist_ok=True)
        for legacy_path in legacy_contents:
            new_path = legacy_path.parent / "legacy" / legacy_path.name
            move(legacy_path, new_path)

    def create_min_settings(self, file_key: str):
        """Create a minimal settings file

        The settings file created contains nothing more than the npc version that will prevent this migration
        from running for this file key.

        Args:
            file_key (str): Key of the settings file to create
        """
        new_settings = self.config_dir_path(file_key) / "settings.yaml"
        data = {
            "npc": {
                "version": self.MINIMUM_VERSION
            }
        }
        with new_settings.open('w', newline="\n") as settings_file:
            yaml.dump(data, settings_file, default_flow_style=False)
