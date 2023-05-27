import click
import os
from pathlib import Path

from click import echo

import npc
from npc.settings import Settings, SubTagSpec
from npc.util import ParseError
from . import presenters, helpers
from .helpers import cwd_campaign
from .errors import CampaignNotFoundException

arg_settings: Settings = Settings()

pass_settings = click.make_pass_decorator(Settings)

###################
# Main entry point
###################

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = npc.settings.app_settings()
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = None
    ctx.max_content_width = term_width

###################
# Campaign init
###################

@cli.command()
@click.option("-n", "--name", help="Campaign name", default="My Campaign")
@click.option("-d", "--desc", help="Description of the campaign", default="Campaign description")
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    required=True,
    help="ID of the game system to use")
@click.argument(
    "campaign_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    default=".")
@pass_settings
def init(settings, campaign_path: Path, name: str, desc: str, system: str):
    """Create the basic folders to set up an npc campaign

    Args: CAMPAIGN_PATH (defaults to current dir)
    """
    campaign_path.mkdir(parents=True, exist_ok=True)
    echo(f"Setting up {campaign_path}...")
    echo("Creating .npc/ config directory")
    echo("Creating required directories:")
    echo(presenters.directory_list(settings.init_dirs))
    npc.campaign.init(
        campaign_path,
        name=name,
        desc=desc,
        system=system,
        settings=settings)
    echo("Done")

###################
# Campaign info
###################

@cli.command()
@pass_settings
def info(settings):
    """Get information about a campaign

    Args: CAMPAIGN_PATH (defaults to current dir)
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    echo(presenters.campaign_info(campaign))

###################
# Browse settings
###################

@cli.command()
@click.option("-l",
    "--location",
    type=click.Choice(["user", "campaign"], case_sensitive=False),
    default="campaign",
    help="The settings file or directory to open. Defaults to campaign.")
@pass_settings
def settings(settings, location):
    """Browse to the campaign or user settings"""
    target_file = helpers.find_or_make_settings_file(settings, location)
    if target_file is None:
        raise CampaignNotFoundException

    click.launch(str(target_file), locate=True)

###################################
# Create and open next session/plot
###################################

@cli.command()
@pass_settings
def session(settings):
    """Create and open the next session and plot file"""
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    new_files = campaign.bump_planning_files()

    npc.util.edit_files(new_files.values(), settings = settings)

##########################
# Open latest session/plot
##########################

@cli.command()
@click.argument("planning_type",
    type=click.Choice(["plot", "session", "both"], case_sensitive=False),
    default="both")
@pass_settings
def latest(settings, planning_type):
    """Find and open the latest plot or session file, or both

    Args: PLANNING_TYPE one of "plot", "session", or "both". (defaults to "both")
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    if planning_type == "both":
        keys = ["plot", "session"]
    else:
        keys = [planning_type]

    files = [campaign.get_latest_planning_file(key) for key in keys]
    npc.util.edit_files(files, settings = settings)

##########################
# Config description group
##########################

@cli.group()
def describe():
    """Show info about systems, types, or tags"""

###################
# Describe systems
###################

@describe.command()
@pass_settings
def systems(settings):
    """Show the configured game systems"""
    systems = [settings.get_system(key) for key in settings.get_system_keys()]
    system_headers = ["Name", "Key", "Description"]
    system_data = [[system.name, system.key, system.desc] for system in systems]
    echo(presenters.tabularize(system_data, headers = system_headers, title = "Configured Systems"))

    campaign = cwd_campaign(settings)
    if campaign:
        echo(f"\nCurrently using {campaign.system.name}")

###################
# Describe types
###################

@describe.command()
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@pass_settings
def types(settings, system):
    """Show the configured character types"""
    campaign = cwd_campaign(settings)
    try:
        if system:
            game_system = settings.get_system(system)
            chartypes = game_system.types
            title = f"Character Types for {game_system.name}"
        elif campaign:
            chartypes = campaign.types
            title = f"Character Types in {campaign.name}"
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    chartype_headers = ["Name", "Key", "Description"]
    chartype_data = [[chartype.name, chartype.key, chartype.desc] for chartype in chartypes.values()]
    echo(presenters.tabularize(chartype_data, headers = chartype_headers, title = title))

###################
# Describe tags
###################

@describe.command()
@click.option("-s", "--system", "system_key",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@click.option("-t", "--type", "type_", help="Show tags for only this character type")
@pass_settings
def tags(settings, system_key, type_):
    """Show the configured tags for this campaign

    Can show the tags available to all character types, or just the ones for a specific type.
    """
    campaign = cwd_campaign(settings)
    try:
        if system_key:
            target = settings.get_system(system_key)
            system = target
        elif campaign:
            target = campaign
            system = campaign.system
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    headers = ["Name", "Description"]
    if type_:
        if type_ not in target.types:
            raise click.BadParameter(f"'{type_}' is not one of {presenters.type_list(target.types)}", param_hint="'-p' / '--type'")

        title = f"Tags for {target.get_type(type_).name} in {target.name}"
        tags = target.type_tags(type_).values()
    else:
        title = f"Tags in {target.name}"
        tags = target.tags.values()
    data = [[tag.name, tag.desc] for tag in tags if not isinstance(tag, SubTagSpec)]
    echo(presenters.tabularize(data, headers = headers, title = title))

####################
# Make new character
####################

@cli.command()
@click.argument("type_key")
@click.option("-n", "--name",
    type=str,
    prompt=True,
    required=True,
    help="Character name")
@click.option("-m", "--mnemonic",
    type=str,
    prompt=True,
    required=True,
    help="One or two words about the character")
@click.option("-d", "--description", "desc",
    type=str,
    help="Bio, background, etc. of the character")
@click.option("-t", "--tag", "tags",
    type=(str, str),
    multiple=True,
    help="Tags to add to the new character, as tagname value pairs.")
@pass_settings
def new(settings, type_key, name, mnemonic, desc, tags):
    """Create a new character

    This command only works within an existing campaign.
    If a name and note are not given, you'll be prompted to add them.

    \b
    Examples:
        npc new supporting -n "Jack Goosington" -m "submariner thief"
        npc new werewolf -n "Howls at Your Face" -m "brat" --tag breed lupus --tag auspice ragabash
        npc new changeling -n "Squawks McGee" -m "flying courier" -t seeming beast -t kith windwing -t court spring

    \b
    Args:
        TYPE_KEY TEXT   Type of the character
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    if type_key not in campaign.types:
        raise click.BadParameter(f"'{type_key}' is not one of {presenters.type_list(campaign.types)}", param_hint="'TYPE_KEY'")

    type_spec = campaign.get_type(type_key)
    body = type_spec.default_sheet_body()

    character_factory = npc.characters.CharacterFactory(campaign)
    character = character_factory.make(
        realname=name,
        mnemonic=mnemonic,
        body=body,
        type_key=type_key,
        desc=desc,
        tags=[npc.characters.RawTag(*t) for t in tags])

    helpers.write_new_character(character, campaign)

    npc.util.edit_files([character.file_path], settings = settings)
