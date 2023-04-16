import click
import logging
from pathlib import Path

from click import echo

import npc
from npc.settings import Settings
from . import presenters
from .helpers import cwd_campaign, find_or_make_settings_file

arg_settings: Settings = Settings()

pass_settings = click.make_pass_decorator(Settings)

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = npc.settings.app_settings()

@cli.command()
@click.option('--name', help="Campaign name", default="My Campaign")
@click.option('--desc', help="Description of the campaign", default="Campaign description")
@click.option('--system',
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    required=True,
    help="ID of the game system to use")
@click.argument(
    'campaign_path',
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

@cli.command()
@pass_settings
def info(settings):
    """Get information about a campaign

    Args: CAMPAIGN_PATH (defaults to current dir)
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        echo("Not a campaign (or any of the parent directories)")
        return

    echo(presenters.campaign_info(campaign))

@cli.command()
@click.option("--location",
    type=click.Choice(["user", "campaign"], case_sensitive=False),
    default="campaign",
    help="The settings file or directory to open. Defaults to campaign.")
@pass_settings
def settings(settings, location):
    """Browse to the campaign or user settings"""
    target_file = find_or_make_settings_file(settings, location)
    if target_file is None:
        echo("Not a campaign (or any of the parent directories)")
        return

    click.launch(str(target_file), locate=True)

@cli.command()
@pass_settings
def session(settings):
    """Create and open the next session and plot file"""
    campaign = cwd_campaign(settings)
    if campaign is None:
        echo("Not a campaign (or any of the parent directories)")
        return

    new_files = campaign.bump_planning_files()

    npc.util.edit_files(new_files.values(), settings = settings)

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
        echo("Not a campaign (or any of the parent directories)")
        return

    if planning_type == "both":
        keys = ["plot", "session"]
    else:
        keys = [planning_type]

    files = [campaign.get_latest_planning_file(key) for key in keys]
    npc.util.edit_files(files, settings = settings)

@cli.group()
def describe():
    """Show info about systems, types, or tags"""

@describe.command()
def systems():
    """Show the configured game systems"""
    print("show the configured game systems")
    # if in a campaign, mark the one in use
    # merge from npc.systems and campaign.systems

@describe.command()
def types():
    """Show the configured character types"""
    print("show the configured types within the current campaign's system, or given system")
    # without campaign, require an explicit system
    # generate from npc.system.x.types merged with campaign.system.x.types

@describe.command()
def tags():
    """Show the configured tags

    Can show the tags available to all character types, or just the ones for a specific type.
    """
    print("show the tags available within this campaign, optionally scoped to a specific system or type")
    # default to campaign system and non-type scoped
    # if not in a campaign, require explicit system
    # if limited to a type, require that the type be in the given system
    # generate from npc.tags; npc.system.x.tags, campaign.system.x.tags; npc.types.x.y.tags, campaign.types.x.y.tags
    # merge down all three to get the tags list
    # same process for deprecated_tags
