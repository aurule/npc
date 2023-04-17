from npc.util import merge_data_dicts
from npc.settings.tags import Tag, make_tags

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
