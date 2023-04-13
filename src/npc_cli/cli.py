import click
import logging
from pathlib import Path

from click import echo

import npc
from npc.settings import Settings
from . import presenters
from .helpers import cwd_campaign

arg_settings: Settings = Settings()

pass_settings = click.make_pass_decorator(Settings, ensure=True)

@click.group()
@click.pass_context
def cli(ctx):
    pass

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
def settings():
    print("open the user or campaign settings.yaml files, or folder with browse flag")

@cli.command()
def session():
    print("create and open new session and plot files")

@cli.command()
def latest():
    print("open the most recent session and/or plot file")

@cli.group()
def describe():
    pass

@describe.command()
def systems():
    print("show info about the configured game systems")

@describe.command()
def types():
    print("show info about the configured types within the current campaign's system, or given system")

@describe.command()
def tags():
    print("show info about the tags available within this campaign, optionally scoped to a specific system or type")
