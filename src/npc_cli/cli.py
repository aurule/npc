import click
import logging
import os
from pathlib import Path

from click import echo

import npc
from npc.settings import Settings, System, SubTag
from npc.util import ParseError
from . import presenters
from .helpers import cwd_campaign, find_or_make_settings_file

arg_settings: Settings = Settings()

pass_settings = click.make_pass_decorator(Settings)

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = npc.settings.app_settings()
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = None
    ctx.max_content_width = term_width

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
            echo("Not a campaign, so the --system option must be provided")
            return 1
    except ParseError as err:
        echo(f"Could not load {err.path}: {err.strerror}")
        return 1

    chartype_headers = ["Name", "Key", "Description"]
    chartype_data = [[chartype.name, chartype.key, chartype.desc] for chartype in chartypes.values()]
    echo(presenters.tabularize(chartype_data, headers = chartype_headers, title = title))

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
            system = settings.get_system(system_key)
            target = system
        elif campaign:
            system = campaign.system
            target = campaign
        else:
            echo("Not a campaign, so the --system option must be provided")
            return 1
    except ParseError as err:
        echo(f"Could not load {err.path}: {err.strerror}")
        return 1

    headers = ["Name", "Description"]
    if type_:
        if type_ not in system.types:
            echo(f"Character type {type_} does not exist in {system.name}")
            return 1

        title = f"Tags for {system.types.get(type_).name} in {target.name}"
        tags = system.type_tags(type_).values()
    else:
        title = f"Tags in {target.name}"
        tags = system.tags.values()
    data = [[tag.name, tag.desc] for tag in tags if not isinstance(tag, SubTag)]
    echo(presenters.tabularize(data, headers = headers, title = title))
