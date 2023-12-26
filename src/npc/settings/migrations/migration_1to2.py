from packaging.version import Version, parse, InvalidVersion
import re
import yaml
from shutil import move
from pathlib import Path

from .settings_migration import SettingsMigration
from .migration_message import MigrationMessage
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

    def migrate(self, file_key: str) -> list[MigrationMessage]:
        """Apply this SettingsMigration to a named settings file

        This migration checks and corrects for a number of settings states:

        1. If a modern settings.yaml exists, but is missing its version, a new version is added.
        2. If no settings files exist at all, a new, minimal file is created. All other contents in the .npc
            directory are moved to a new legacy/ folder.
        3. If a legacy settings file exists, its data is used to populate a new settings.yaml file. All other
            contents in the .npc directory are moved to a new legacy/ folder.

        Args:
            file_key (str): Key of the settings file to modify

        Returns:
            list: List of MigrationMessage objects detailing the changes made
        """

        if self.modern_format(file_key):
            self.update_version(file_key, self.MINIMUM_VERSION)
            version_message = MigrationMessage(
                f"Updated version to {self.MINIMUM_VERSION}",
                file=self.path_for_key(file_key),
                key="npc.version")
            return [version_message]

        legacy_data = self.load_legacy(file_key)
        self.archive_legacy_files(file_key)
        if not legacy_data:
            self.create_min_settings(file_key)
            file_message = MigrationMessage(
                "Created missing file",
                file=self.path_for_key(file_key))
            return [file_message]

        return self.convert(file_key, legacy_data)

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

        legacy_dir = settings_dir.joinpath("legacy")
        legacy_dir.mkdir(exist_ok=True)
        for legacy_path in legacy_contents:
            new_path = legacy_dir / legacy_path.name
            move(legacy_path, new_path)

    def legacy_path(self, file_key: str) -> Path:
        """Get the path to the legacy files archive

        Args:
            file_key (str): Key of the settings location to access

        Returns:
            Path: Path to the legacy archive dir
        """
        return self.config_dir_path(file_key) / "legacy"

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
        with new_settings.open("w", newline="\n") as settings_file:
            yaml.dump(data, settings_file, default_flow_style=False)

    def convert(self, file_key: str, legacy_data: DataStore) -> list[MigrationMessage]:
        messages = []
        version_data = {
            "npc": {
                "version": self.MINIMUM_VERSION
            }
        }
        new_data = DataStore(version_data)
        new_data.merge_data(self.convert_legacy_keys(legacy_data))
        new_data.merge_data(self.convert_listing_sort(legacy_data))
        new_data.merge_data(self.convert_ignores(legacy_data))
        new_data.merge_data(self.convert_session_templates(file_key, legacy_data))
        new_settings = self.config_dir_path(file_key) / "settings.yaml"
        with new_settings.open("w", newline="\n") as settings_file:
            yaml.dump(new_data.data, settings_file, default_flow_style=False)

        messages.extend(self.convert_type_templates(file_key, legacy_data))

        if self.legacy_path(file_key).joinpath("listing").exists():
            messages.append(MigrationMessage(
                "Mako templates are no longer supported. You will need to recreate them using Jinja."
            ))

        if legacy_data.get("paths.hierarchy"):
            messages.append(MigrationMessage(
                "The 'paths.hierarchy' key is replaced by 'campaign.subpath_components'. You will need to convert your path spec manually."
            ))

        messages.append(MigrationMessage(
            "The meta-fields like `type-social` used in the old path.hierarchy string have been removed. You should check your character paths to make sure they're still correct."
        ))
        messages.append(MigrationMessage(
            "Some tags have changed. You should run the linter to see what's outdated."
        ))

        return messages

    def convert_legacy_keys(self, legacy_data: DataStore) -> DataStore:
        """Convert simple legacy keys to their new location

        This only handles those legacy keys whose values are still valid, but need to be written to a new key.

        Args:
            legacy_data (DataStore): The old data to convert

        Returns:
            DataStore: Store with the converted legacy key data
        """
        key_map = {
            "campaign_name": "campaign.name",
            "editor": "npc.editor",
            "paths.required.additional_paths": "campaign.create_on_init",
            "listing.default_format": "campaign.listing.format",
            "listing.sort_by": "campaign.listing.sort_by",
            "listing.base_header_level": "campaign.listing.base_header_level",
            "listing.metadata.title": "campaign.listing.metadata.title",
            "listing.metadata.timestamp": "campaign.listing.metadata.timestamp",
        }

        new_data = DataStore()

        for (old_key, new_key) in key_map.items():
            if old_val := legacy_data.get(old_key):
                new_data.set(new_key, old_val)

        return new_data

    def convert_listing_sort(self, legacy_data: DataStore) -> DataStore:
        """Convert old listing sort values to new ones

        This both replaces old pseudo-tags (last, first, name) with new ones, and moves the sort values to the
        new group_by and sort_by keys.

        Args:
            legacy_data (DataStore): The old data to convert

        Returns:
            DataStore: Store with the converted listings data
        """
        specials_map = {
            "last": "last_name",
            "first": "first_name",
            "name": "full_name",
        }

        new_data = DataStore()

        if old_sort := legacy_data.get("listing.sort_by"):
            updated_sort = [specials_map.get(s, s) for s in old_sort]
            new_data.set("campaign.listing.group_by", updated_sort)
            new_data.set("campaign.listing.sort_by", updated_sort)

        return new_data

    def convert_ignores(self, legacy_data: DataStore) -> DataStore:
        """Convert old globally ignored character paths

        The old paths required a Characters/ prefix, which is stripped from the new paths.

        Args:
            legacy_data (DataStore): The old data to convert

        Returns:
            DataStore: Store with the converted ignored character paths
        """
        new_data = DataStore()

        campaign_base = self.settings.campaign_dir
        if not campaign_base:
            return new_data

        character_base = campaign_base / self.settings.get("campaign.characters.path")

        if old_ignores := legacy_data.get("paths.ignore.always"):
            new_ignores = [ str(
                               campaign_base \
                               .joinpath(old_ignore) \
                               .relative_to(character_base)
                            ) for old_ignore in old_ignores]
            new_data.set("campaign.characters.ignore_subpaths", new_ignores)

        return new_data

    def convert_session_templates(self, file_key: str, legacy_data: DataStore) -> DataStore:
        """Convert old plot and session templates to new format

        The old filenames from story.templates.session (and .plot) are slightly tweaked to replace the NNN
        constant with the new ((NNN)). The total number of Ns remains the same, as it doesn't matter. THey're
        then stored in campaign.session.filename_pattern.

        Each file's contents are read in and stored as-is into campaign.session.file_contents.

        If the legacy key is missing, the new key is not generated. If the key is present but not the file,
        the key will be converted and the file contents will not be populated. This is useful for setting a
        preferred filename format without changing the default contents.

        Args:
            file_key (str): Key of the settings file we're converting
            legacy_data (DataStore): The old data to convert

        Returns:
            DataStore: Store with the converted session and plot template data
        """
        nn_re = re.compile(r"(NN+)")
        def old_to_new(key: str):
            if old_thing := legacy_data.get(f"story.templates.{key}"):
                new_thing = nn_re.sub(r"((\1))", old_thing)
                new_data.set(f"campaign.{key}.filename_pattern", new_thing)
                old_path = self.legacy_path(file_key) / old_thing
                if old_path.exists():
                    with old_path.open("r") as f:
                        new_data.set(f"campaign.{key}.file_contents", f.read())

        new_data = DataStore()

        old_to_new("session")
        old_to_new("plot")

        return new_data

    def convert_type_templates(self, file_key: str, legacy_data: DataStore) -> list[MigrationMessage]:
        messages: list[MigrationMessage] = []

        types_dir = self.config_dir_path(file_key) / "types"
        legacy_path = self.legacy_path(file_key)

        old_types = legacy_data.get("types", [])
        if old_types:
            types_dir.mkdir(exist_ok=True)
        for old_typekey in old_types:
            old_template = legacy_data.get(f"types.{old_typekey}.sheet_template")
            if not old_template:
                continue

            old_path = legacy_path / old_template
            if not old_path.exists():
                continue

            new_path = types_dir / f"{old_typekey}{old_path.suffix}"
            with old_path.open("r") as old_file:
                with new_path.open("w", newline="\n") as new_file:
                    new_file.write(old_file.read())
            messages.append(MigrationMessage(
                f"Created {old_typekey} sheet template from {old_template}. You may want to change the new template's suffix.",
                file=new_path
            ))

        return messages
