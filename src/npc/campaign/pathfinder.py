from pathlib import Path

from .campaign_class import Campaign
from ..characters import Character

def build_character_path(character: Character, campaign: Campaign, existing: bool = True) -> Path:
    character_path = campaign.characters_dir
    components = campaign.settings.get("campaign.characters.subpath_components")
    for component in components:
        match component["selector"]:
            case "first_value":
                pass
                # if existing,
                #   get all values for named tag(s) from character
                #   iterate those values
                #       if existing and value is a dir under character_path, add value to character_path
                # else
                #   get first value for named tag(s) from character
                #   if no value, move on
                #   add that value to character_path
            case _:
                pass
                # unsupported selector
