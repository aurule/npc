from sqlalchemy import Select
from pathlib import Path

from npc.util import win_sanitize
from .campaign_class import Campaign
from ..characters import Character, Tag
from ..db import DB, character_repository

class Pathfinder:
    """Class for finding and manipulating character-specific paths"""

    def __init__(self, campaign: Campaign, db: DB = None):
        self.campaign = campaign
        self.path_components = campaign.settings.get("campaign.characters.subpath_components")
        self.base_path = campaign.characters_dir

        if not db:
            self.db = DB()
        else:
            self.db = db

    def build_character_path(self, character: Character, *, exists: bool = True) -> Path:
        """Construct a character path based on the campaign settings

        The path is built using the saved subpath components from our campaign's settings.

        Args:
            character (Character): The character whose path to make
            exists (bool): Whether to limit paths to directories that already exist (default: `True`)

        Returns:
            Path: Path for the character file. This is only a directory! No filename is included.

        Raises:
            KeyError: Raised if the tags key is missing from a subpath component
            ValueError: Raised if the subpath component's selector is not found or not recognized
        """
        character_path: Path = self.base_path
        for component in self.path_components:
            match component.get("selector"):
                case "first_value":
                    tag_names = component.get("tags")
                    if not tag_names:
                        raise KeyError("Missing tags key for subpath component")

                    stmt: Select = character_repository.tag_values_by_name(character, *tag_names)

                    if exists:
                        existing_dirs: list = [child.name for child in character_path.iterdir() if child.is_dir()]
                        stmt = stmt.where(Tag.value.in_(existing_dirs))

                    with self.db.session() as session:
                        result_tag = session.execute(stmt).first()

                    if result_tag:
                        character_path = character_path.joinpath(result_tag[0])
                case _:
                    raise ValueError("Invalid subpath component selector")

        return character_path

    def make_filename(self, character: Character) -> str:
        """Create a filename using a character's attributes

        Sanitizes the name and mnemonic, then uses them to make a new filename. The format is
        "name - mnemonic.npc".

        Args:
            character (Character): Character to make a filename for

        Returns:
            str: The generated filename
        """
        sanitized_name = win_sanitize(character.name)
        sanitized_mnemonic = win_sanitize(character.mnemonic)
        return f"{sanitized_name} - {sanitized_mnemonic}.npc"
