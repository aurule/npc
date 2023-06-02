import os
from pathlib import Path

import npc
from npc.db import DB
from npc.settings import Settings
from npc.campaign import Campaign, Pathfinder
from npc.characters import Character, RawTag, CharacterWriter

import logging
logger = logging.getLogger(__name__)

def cwd_campaign(settings: Settings) -> Campaign:
    """Make a campaign object for the nearest campaign to the current dir

    If the current dir or any of its parents is a campaign, return a new Campaign object. Otherwise, warn and
    return None.

    Args:
        settings (Settings): Settings file to use when constructing the campaign

    Returns:
        Campaign: New campaign object for the found dir
    """
    campaign_root = npc.campaign.find_campaign_root(os.getcwd())
    if not campaign_root:
        logger.info("Not a campaign (or any of the parent directories)")
        return None
    logger.info(f"Found campaign root at {campaign_root}")

    return Campaign(campaign_root, settings = settings)

def find_or_make_settings_file(settings: Settings, location: str) -> str:
    """Find or create the desired settings file, if possible

    Looks for either the user or campaign settings file.

    The user file is pulled from settings.personal_dir. The campaign file is found by first locating the
    nearest actual campaign. If there is none, then this function aborts and returns None.

    If the target file exists, its path is returned as a string. If it does not, the file is created along
    with all parents and populated with a minimal dict.

    Args:
        settings (Settings): [description]
        location (str): [description]

    Returns:
        str: [description]
    """
    valid_locations: list[str] = ["user", "campaign"]
    if location not in valid_locations:
        logger.error(f"Unrecognized settings location '{location}'")
        return None

    if location == "user":
        target_file = settings.personal_dir / "settings.yaml"
    else:
        campaign = cwd_campaign(settings)
        if campaign is None:
            return
        target_file = campaign.settings_file

    if not target_file.exists():
        target_file.parent.mkdir(exist_ok=True, parents=True)
        target_file.write_text("npc: {}", newline="\n")

    return str(target_file)

def write_new_character(character: Character, campaign: Campaign, db=None):
    """Create a new character file

    This function determines the correct file path and name for the given character object, then writes its
    tags and default sheet body to that file. It also adds the character to the database, but that is
    incidental.

    The Character object's file_path is directly modified.

    Args:
        character (Character): Character to create
        campaign (Campaign): Campaign containing the character
        db (DB): Optional database to use. Intended for dependency injection during testing.
    """
    if not db:
        db = DB()

    with db.session() as session:
        session.add(character)
        session.commit()

        finder = Pathfinder(campaign, db=db)
        sheet_path: Path = finder.build_character_path(character)
        sheet_name: str = finder.make_filename(character)

        character.file_path = sheet_path / sheet_name
        session.commit()

    writer = CharacterWriter(campaign, db=db)
    writer.write(character)
