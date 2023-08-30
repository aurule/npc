from packaging.version import Version, parse, InvalidVersion

from .settings_migration import SettingsMigration

class Migration1to2(SettingsMigration):
    def should_apply(self, file_key: str) -> bool:
        """Whether this SettingsMigration should run on the given settings file

        This will often involve using packaging.version to compare version numbers from settings.versions.

        Args:
            file_key (str): Key of the settings file to check

        Returns:
            bool: True if this SettingsMigration should be run on the given file, False if not
        """
        settings_version = self.version_for_key(file_key)
        minimum_version = Version("2.0.0")
        return settings_version < minimum_version

    def migrate(self, file_key: str):
        """Apply this SettingsMigration to a named settings file

        The file location is stored in settings.loaded_files. If the SettingsMigration succeeds, this method should
        always alter the file such that should_apply returns False in the future. This usually means updating
        the npc.version string to some minimum version.

        Args:
            file_key (str): Key of the settings file to modify
        """
        pass
        # we're given a file_key




        # if there is no json and no yaml file:
        #   create a minimal settings.yaml with npc.version and a comment explaining the missing components
        # if there is an existing json file:
        # create a yaml file from the existing json file
        #   translate keys using legacy_keys.yaml
        #   warn about custom templates being incompatible and needing to be converted
        #   paths.hierarchy is replaced by campaign.subpath_components system
        #       Either convert automatically, or warn the user will need to replace it
        #   types.key.sheet_template files need to go in a new dir with new names
        #   plot and session files now have contents stored in settings file
        #       maybe move automatically?
        #   handle deprecated tags
        #   listing.sort_by convert old constant values to new ones

    @property
    def sequence(self) -> int:
        """This migration is always first

        Returns:
            int: The sequence number of the SettingsMigration
        """
        return 0
