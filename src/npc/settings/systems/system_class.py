from functools import cached_property

from npc.util import merge_data_dicts
from npc.settings.tags import make_tags
from npc.settings.types import make_types

class System():
    """Represents a game system"""

    def __init__(self, key: str, settings):
        self.key: str = key
        system_def = settings.get(f"npc.systems.{key}")
        if system_def is None:
            raise KeyError(f"No system named '{key}' is defined")

        self.name: str = system_def["name"]
        self.desc: str = system_def["desc"]
        self.settings = settings

    @property
    def types_dir(self):
        """Get the path to the directory where types are defined for this system

        Returns:
            Path: Path to the main types definition dir
        """
        return self.settings.default_settings_path / "types" / self.key

    @cached_property
    def types(self) -> dict:
        """Get the character types for this system

        The character types here are only those described at the global level -- i.e. from the default and user
        settings. Campaign-level types are handled by the Campaign class.

        Returns:
            dict: Dict of character type objects
        """
        self.settings.load_types(self.types_dir, system_key=self.key)
        return make_types(self.settings.get(f"npc.types.{self.key}"))

    @cached_property
    def tags(self) -> dict:
        """Get the tags configured for this system

        Combines tag definitions from the core npc namespace as well as this system.

        Returns:
            dict: Dict of Tag objects
        """
        core_tag_defs: dict = self.settings.get("npc.tags")
        system_tag_defs: dict = self.settings.get(f"npc.systems.{self.key}.tags", {})
        combined_defs: dict = merge_data_dicts(core_tag_defs, system_tag_defs)
        return make_tags(combined_defs)
