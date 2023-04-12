import click
from pathlib import Path

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
    npc.campaign.init(campaign_path, name=name, desc=desc, system=system, settings=settings)

@cli.command()
def describe():
    print("describe the configured game systems, or types")

@cli.command()
def session():
    print("create and open new session and plot files")

@cli.command()
def latest():
    print("open the most recent session and/or plot file")

@cli.command()
def settings():
    print("open the user or campaign settings.yaml files")
