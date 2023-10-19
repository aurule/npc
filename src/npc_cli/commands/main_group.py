import click
from os import get_terminal_size
from packaging.version import Version

from npc import __version__ as npc_version
from npc.settings import Settings, app_settings
from npc_cli.helpers import try_migrating

arg_settings: Settings = app_settings()

pass_settings = click.make_pass_decorator(Settings)

###################
# Main entry point
###################

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = app_settings()
    try:
        term_width = get_terminal_size().columns
    except OSError:
        term_width = None
    ctx.max_content_width = term_width

    ctx.show_default = True

    # check that we aren't outdated
    our_version = Version(npc_version)
    settings_version = Version(arg_settings.versions.get("user", npc_version))
    if our_version < settings_version:
        click.echo(f"WARNING: Installed version of NPC ({our_version}) is older than the one which last updated your user settings ({settings_version}). NPC may behave incorrectly. Please upgrade to the latest release as soon as possible.")

    # migrate user settings
    try_migrating(arg_settings, "user")
