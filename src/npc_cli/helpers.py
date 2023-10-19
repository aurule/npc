import os
import click
from pathlib import Path
from packaging.version import Version

import npc
from npc.db import DB
from npc.settings import Settings
from npc.campaign import Campaign, Pathfinder
from npc.characters import Character, RawTag, CharacterWriter
from npc.settings.migrations import SettingsMigrator
from npc import __version__ as npc_version
from npc_cli.errors import CampaignNotFoundException

import logging
logger = logging.getLogger(__name__)

def get_campaign(settings: Settings) -> Campaign:
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

    campaign = Campaign(campaign_root, settings = settings)
    check_outdated(settings, "campaign")
    try_migrating(settings, "campaign")

    return campaign

def campaign_or_fail(settings: Settings) -> Campaign:
    """Get the nearest campaign or raise an exception

    If the current dir or any of its parents is a campaign, return a new Campaign object. Otherwise, raise
    a CampaignNotFoundException error to abort the script.

    Args:
        settings (Settings): Settings file to use when constructing the campaign

    Returns:
        Campaign: New campaign object for the found dir

    Raises:
        CampaignNotFoundException: Raised when a campaign dir cannot be found
    """
    campaign = get_campaign(settings)

    if campaign is None:
        raise CampaignNotFoundException

    return campaign

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
        campaign = get_campaign(settings)
        if campaign is None:
            return
        target_file = campaign.settings_file

    if not target_file.exists():
        target_file.parent.mkdir(exist_ok=True, parents=True)
        target_file.write_text("npc: {}", newline="\n")

    return str(target_file)

def check_outdated(settings: Settings, location: str):
    """Check if a loaded settings file is from a newer version of NPC

    This function just prints a warning statement and does not prevent execution of commands. NPC is intended
    to be strongly backwards compatable within major versions, with breaking changes to settings handled by
    the migration system.

    Args:
        settings (Settings): Settings object to check
        location (str): Settings location to check. One of "user" or "campaign".
    """

    # Skip outdated warning during testing. The cli tests often run with
    # intentionally incomplete or incorrect settings.
    if "PYTEST_CURRENT_TEST" in os.environ:
        return

    our_version = Version(npc_version)
    settings_version = Version(settings.versions.get(location, npc_version))
    if our_version < settings_version:
        click.echo(f"WARNING: Installed version of NPC ({our_version}) is older than the one which last updated your {location} settings ({settings_version}). NPC may behave incorrectly. Please upgrade to the latest release as soon as possible.")

def try_migrating(settings: Settings, location: str):
    """Test settings for migration and prompt to migrate

    This method ensures the user is aware if their personal or campaign settings are out of date, and gives
    the opportunity to apply pending migrations. Running commands is blocked unless migrations are run, to
    prevent unexpected behavior.

    Args:
        settings (Settings): Settings object to check
        location (str): Settings location to check. One of "user" or "campaign".
    """

    # Skip migration prompt during testing. The cli tests often run with
    # intentionally incomplete or incorrect settings.
    if "PYTEST_CURRENT_TEST" in os.environ:
        return

    migrator = SettingsMigrator(settings)
    if migrator.can_migrate(location):
        action = click.prompt(
            f"Your {location} settings are out of date and need to be migrated. Do you want to migrate now, open the files for manual inspection, or quit NPC",
            default="migrate",
            type=click.Choice(["migrate", "open", "quit"])
        )
        match action:
            case "migrate":
                click.echo("Migrating...")
                messages = migrator.migrate(location)
                for m in messages:
                    click.echo(m.message)
                click.echo("Done migrating!\n")
            case "open":
                click.launch(str(arg_settings.loaded_paths.get(location)), locate=True)
                raise click.ClickException()
            case _:
                raise click.ClickException()

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
