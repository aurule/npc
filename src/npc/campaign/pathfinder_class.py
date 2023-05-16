from sqlalchemy import Select
from pathlib import Path

from .campaign_class import Campaign
from ..characters import Character, Tag
from ..db import DB

class Pathfinder:
    def __init__(self, campaign: Campaign, db: DB = None):
        self.campaign = campaign
        self.path_components = campaign.settings.get("campaign.characters.subpath_components")
        self.base_path = campaign.characters_dir

        if not db:
            self.db = DB()
        else:
            self.db = db

    def build_character_path(self, character: Character, *, exists: bool = True) -> Path:
        character_path: Path = self.base_path
        for component in self.path_components:
            match component.get("selector"):
                case "first_value":
                    tag_names = component.get("tags")
                    if not tag_names:
                        raise KeyError("Missing tags key for supath component")

                    stmt: Select = character.tag_value_query(*tag_names)

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
