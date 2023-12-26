import click
from click import echo
from pathlib import Path

import npc
from npc_cli.presenters import directory_list, campaign_info
from npc_cli.helpers import campaign_or_fail, find_or_make_settings_file
from npc_cli.errors import CampaignNotFoundException

from .main_group import cli, arg_settings, pass_settings

###################
# Campaign init
###################

@cli.command()
@click.option("-n", "--name", help="Campaign name", prompt="Campaign name")
@click.option("-d", "--desc", help="Description of the campaign", prompt="Campaign description")
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    prompt="Game system",
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
    echo(directory_list(settings.init_dirs))
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
    """
    campaign = campaign_or_fail(settings)

    echo(campaign_info(campaign))

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
    target_file = find_or_make_settings_file(settings, location)
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
    campaign = campaign_or_fail(settings)

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
    campaign = campaign_or_fail(settings)

    if planning_type == "both":
        keys = ["plot", "session"]
    else:
        keys = [planning_type]

    files = [campaign.get_latest_planning_file(key) for key in keys]
    npc.util.edit_files(files, settings = settings)
