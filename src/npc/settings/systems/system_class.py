from functools import cached_property, cache

from npc.util import merge_data_dicts
from npc.settings.tags import make_tags, make_metatags, TagSpec, UndefinedTagSpec
from npc.settings.types import make_types, TypeSpec, UndefinedTypeSpec
from npc.settings.tag_definer_interface import TagDefiner

@TagDefiner.register
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

    def get_type(self, type_key: str) -> TypeSpec:
        """Get a single character type

        Args:
            type_key (str): Key for the character type to get

        Returns:
            TypeSpec: TypeSpec for the given key, or an UndefinedTypeSpec if that key does not have a type
        """
        return self.types.get(type_key, UndefinedTypeSpec(type_key))

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
            dict: Dict of TagSpec objects indexed by tag key
        """
        return make_tags(self.system_tag_defs)

    def get_tag(self, tag_name: str) -> TagSpec:
        """Get a single tag as configured for this system

        Uses the combied core and system definitions

        Args:
            tag_name (str): Name of the tag to get

        Returns:
            TagSpec: Spec of the named tag, or a new UndefinedTagSpec if that tag has no definition
        """
        return self.tags.get(tag_name, UndefinedTagSpec(tag_name))

    @property
    def system_metatag_defs(self) -> dict:
        """Get the combined metatag definitions for this system

        Merges the system-specific metatags into the global metatags and returns the resulting dict

        Returns:
            dict: Dict of metatag configurations
        """
        core_tag_defs: dict = self.settings.get("npc.metatags", {})
        system_tag_defs: dict = self.settings.get(f"npc.systems.{self.key}.metatags", {})
        return merge_data_dicts(system_tag_defs, core_tag_defs)

    @cached_property
    def metatags(self) -> dict:
        """Get the metatags configured for this system

        Combines metatag definitions from the core npc namespace as well as this system.

        Returns:
            dict: Dict of MetatagSpec objects indexed by tag key
        """
        return make_metatags(self.system_metatag_defs)

    @cache
    def type_tags(self, type_key: str) -> dict:
        """Get the tags for a specific character type

        Combines core and system tags with any tags defined in the type itself

        Args:
            type_key (str): Key for the character type to get tags for

        Returns:
            dict: Dict of TagSpec objects indexed by tag key
        """
        char_type = self.get_type(type_key)

        type_tag_defs: dict = char_type.definition.get("tags", {})
        combined_defs = merge_data_dicts(type_tag_defs, self.system_tag_defs)
        return make_tags(combined_defs)
