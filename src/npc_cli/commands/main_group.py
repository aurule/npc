import click
from os import get_terminal_size
from packaging.version import Version

from npc import __version__ as npc_version
from npc.settings import Settings, app_settings
from npc.settings.migrations import SettingsMigrator

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
    migrator = SettingsMigrator(arg_settings)
    if migrator.can_migrate("user"):
        action = click.prompt(
            f"Your user settings are out of date and need to be migrated. Do you want to migrate now, open the files for manual inspection, or quit NPC",
            default="migrate",
            type=click.Choice(["migrate", "open", "quit"])
        )
        match action:
            case "migrate":
                click.echo("Migrating...")
                messages = migrator.migrate("user")
                for m in messages:
                    click.echo(m.message)
                click.echo("Done migrating!\n")
            case "open":
                click.launch(str(arg_settings.personal_dir / "settings.yaml"), locate=True)
                ctx.exit(1)
            case _:
                ctx.exit(1)
