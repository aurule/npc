from sqlalchemy import select
from pathlib import Path

from .campaign_class import Campaign
from ..characters import Character, Tag
from ..db import DB

class Pathfinder:
    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self.path_components = campaign.settings.get("campaign.characters.subpath_components")
        self.base_path = campaign.characters_dir

    def build_character_path(self, character: Character, *, exists: bool = True) -> Path:
        character_path: Path = self.base_path
        for component in self.path_components:
            match component.get("selector"):
                case "first_value":
                    stmt = select(Tag).where(Tag.name.in_(component.get("tags", []))).order_by(Tag.id)

                    if exists:
                        existing_dirs = [child for child in character_path.iterdir() if child.is_dir()]
                        stmt = stmt.where(Tag.value.in_(existing_dirs))

                    db = DB()
                    with db.session() as session:
                        result_tag = session.execute(stmt).first()

                    if result_tag:
                        print(character_path.joinpath(result_tag[0].value))
                        character_path = character_path.joinpath(result_tag[0].value)
                case _:
                    pass
                    # unsupported selector

        return character_path
