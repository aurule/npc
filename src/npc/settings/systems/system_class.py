from functools import cached_property, cache

from npc.util import merge_data_dicts
from npc.settings.tags import make_tags
from npc.settings.types import make_types, UndefinedType

class System():
    """Represents a game system"""

    def __init__(self, key: str, settings):
        self.key: str = key
        system_def = settings.get(f"npc.systems.{key}")
        if system_def is None:
            raise KeyError(f"No system named '{key}' is defined")

        self.name: str = system_def.get("name", "")
        self.desc: str = system_def.get("desc", "")
        self.extends: str = system_def.get("extends")
        self.settings = settings

    def __hash__(self) -> int:
        """Get a hash for this system

        Generates a hash based on the system key and the settings file it's associated with.

        Returns:
            int: Hash of this system's key and settings
        """
        return hash((self.key, self.name, self.desc, self.extends, self.settings))

    def __eq__(self, other) -> bool:
        """Test whether this system is the same as another system

        Args:
            other (System): System to test against

        Returns:
            bool: True if both systems' hashes match, False if not
        """
        if not isinstance(other, System):
            return NotImplemented

        return hash(self) == hash(other)

    def __ne__(self, other) -> bool:
        """Test whether this sytem is not the same as nother system

        Args:
            other (System): System to test against

        Returns:
            bool: False if both systems' hashes match, True if not
        """
        return not(self == other)

    @cached_property
    def parent(self):
        """Get the parent system, if this system has one

        If this system has the extends property, get the System object for its parent system. Otherwise,
        returns None.

        Returns:
            System: The parent system of this game system, or None if no parent is defined
        """
        if not self.extends:
            return None
        return self.settings.get_system(self.extends)

    @property
    def types_dir(self):
        """Get the path to the directory where default types are defined for this system

        Returns:
            Path: Path to the main types definition dir
        """
        return self.settings.default_settings_path / "types" / self.key

    @property
    def personal_types_dir(self):
        """Get the path to the directory where user types are defined

        Returns:
            Path: Path to the usesr types definition dir
        """
        return self.settings.personal_dir / "types" / self.key

    @cache
    def load_types(self):
        """Load the character type definitions for this system

        Merges in the type definition files in the default and user settings. If this system extends another,
        the parent's types will also be loaded into the parent's namespace.
        """
        if self.parent:
            self.parent.load_types()
        self.settings.load_types(self.types_dir, system_key = self.key)
        self.settings.load_types(self.personal_types_dir, system_key = self.key)

    @property
    def typedefs(self) -> dict:
        self.load_types()
        own_defs = self.settings.get(f"npc.types.{self.key}", {})
        if self.parent:
            return merge_data_dicts(own_defs, self.parent.typedefs)
        else:
            return own_defs

    @property
    def types(self) -> dict:
        """Get the character types for this system

        The character types here are only those described in the default and user settings. Campaign-level
        types are handled by the Campaign class.

        Returns:
            dict: Dict of character type objects
        """
        return make_types(self.typedefs)

    @property
    def system_tag_defs(self) -> dict:
        """Get the combined tag definitions for this system

        Merges the system-specific tags into the global tags and returns the resulting dict

        Returns:
            dict: Dict of tag configurations
        """
        core_tag_defs: dict = self.settings.get("npc.tags")
        system_tag_defs: dict = self.settings.get(f"npc.systems.{self.key}.tags", {})
        return merge_data_dicts(system_tag_defs, core_tag_defs)

    @cached_property
    def tags(self) -> dict:
        """Get the tags configured for this system

        Combines tag definitions from the core npc namespace as well as this system.

        Returns:
            dict: Dict of Tag objects
        """
        return make_tags(self.system_tag_defs)

    @cache
    def type_tags(self, type_key) -> dict:
        char_type = self.types.get(type_key, UndefinedType())

        type_tag_defs: dict = char_type.definition.get("tags", {})
        combined_defs = merge_data_dicts(type_tag_defs, self.system_tag_defs)
        return make_tags(combined_defs)
