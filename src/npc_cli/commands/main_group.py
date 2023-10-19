import click
from os import get_terminal_size

from npc.settings import Settings, app_settings
from npc_cli.helpers import check_outdated, try_migrating

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

    check_outdated(arg_settings, "user")
    try_migrating(arg_settings, "user")
