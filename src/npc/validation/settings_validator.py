from npc.validation.errors.settings_errors import *
from npc.settings import Settings
from npc.settings.helpers import quiet_parse
from npc.util import DataStore

class SettingsValidator:
    """Validator for settings correctness

    This validator checks that the loaded settings are minimally correct
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    def validate(self) -> list:
        """Check our settings for major errors

        This checks for:
        * locked tags are not redefined by non-core files
        * npc.version is present in every loaded file

        Returns:
            list: List of ValidationError objects
        """
        errors: list = []

        compiled_settings = DataStore()
        for settings_key, settings_path in self.settings.loaded_paths.items():
            if not settings_path:
                continue

            loaded: dict = quiet_parse(settings_path)
            if loaded is None:
                continue

            step_settings = DataStore(loaded)

            if not step_settings.get("npc.version"):
                errors.append(SettingsNoVersionError(settings_path))
            for tag_name, tag_def in step_settings.get("npc.tags", {}).items():
                if compiled_settings.get(f"npc.tags.{tag_name}.locked", False):
                    errors.append(SettingsLockedTagError(tag_name, settings_path))

            compiled_settings.merge_data(step_settings)

        return errors
