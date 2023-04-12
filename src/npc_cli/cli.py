import click
import logging
from pathlib import Path

from click import echo

import npc
from npc.settings import Settings

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
    echo("Creating the following required directories:")
    echo(settings.init_dirs)
    npc.campaign.init(
        campaign_path,
        name=name,
        desc=desc,
        system=system,
        settings=settings)
    echo("Done")

@cli.command()
@click.argument(
    'campaign_path',
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    default=".")
@pass_settings
def info(settings, campaign_path: Path):
    campaign_root = npc.campaign.find_campaign_root(campaign_path)
    if not campaign_root:
        echo(f"No campaign seems to contain {campaign_path}")
        return
    logging.info(f"Found campaign root at {campaign_root}")

    campaign = npc.campaign.Campaign(campaign_root, settings = settings)
    echo(campaign.name)
    echo(campaign.desc)
    echo(campaign.system_key)
    echo(campaign.latest_plot_index)
    echo(campaign.latest_session_index)

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
