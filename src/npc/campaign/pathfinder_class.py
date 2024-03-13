from functools import cache
from sqlalchemy import Select
from pathlib import Path

from npc.util import win_sanitize
from npc.characters import CharacterReader, Character, Tag
from npc.db import DB, character_repository
from .subpath_components import get_component

class Pathfinder:
    """Class for finding and manipulating character-specific paths"""

    def __init__(self, campaign, db: DB = None):
        self.campaign = campaign
        self.db = db if db else DB()

    def build_character_path(self, character: Character, *, exists: bool = True) -> Path:
        """Construct a character path based on the campaign settings

        The path is built using the saved subpath components from our campaign's settings.

        Args:
            character (Character): The character whose path to make
            exists (bool): Whether to limit paths to directories that already exist (default: `True`)

        Returns:
            Path: Path for the character file. This is only a directory! No filename is included.
        """
        character_path: Path = self.campaign.characters_dir
        for component in self.make_component_stack(exists):
            component_value = component.value(character, character_path)
            if component_value:
                character_path = character_path.joinpath(component_value)

        return character_path

    def make_filename(self, character: Character) -> str:
        """Create a filename using a character's attributes

        Sanitizes the name and mnemonic, then uses them to make a new filename. The format is
        "name - mnemonic.npc". The suffix used is based on the character type's default sheet. See
        TypeSpec.default_sheet_suffix.

        Args:
            character (Character): Character to make a filename for

        Returns:
            str: The generated filename
        """
        sanitized_name = win_sanitize(character.name)
        sanitized_mnemonic = win_sanitize(character.mnemonic)

        type_spec = self.campaign.get_type(character.type_key)
        suffix = type_spec.default_sheet_suffix

        if not sanitized_name:
            return ""

        parts = [sanitized_name]
        if sanitized_mnemonic:
            parts.append(CharacterReader.NAME_SEPARATOR)
            parts.append(sanitized_mnemonic)
        parts.append(suffix)

        return "".join(parts)

    @cache
    def make_component_stack(self, exists: bool) -> list:
        """Create a stack of subpath component objects

        These can then be iterated repeatedly to apply their rules to multiple characters.

        Args:
            exists (bool): Whether to limit paths to directories that already exist

        Returns:
            list: List of subpath component objects

        Raises:
            ValueError: Raised if the subpath component's selector is not found or not recognized
        """
        comps = []

        for spec in self.campaign.settings.get("campaign.characters.subpath_components"):
            klass = get_component(spec.get("selector"))
            if klass:
                comps.append(klass(self.db, spec, exists))
            else:
                raise ValueError("Invalid subpath component selector")

        return comps
