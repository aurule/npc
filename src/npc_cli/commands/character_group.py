import click
import io
from click import echo, BadParameter

from npc import characters, linters, listers
from npc.util import edit_files
from npc_cli.presenters import type_list
from npc_cli.helpers import cwd_campaign, write_new_character
from npc_cli.errors import CampaignNotFoundException, BadCharacterTypeException

from .main_group import cli, pass_settings

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
    If a name and mnemonic are not given, you'll be prompted to add them.

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
        raise BadCharacterTypeException(type_key, type_list(campaign.types), "'TYPE_KEY'")

    type_spec = campaign.get_type(type_key)
    body = type_spec.default_sheet_body()

    character_factory = characters.CharacterFactory(campaign)
    character = character_factory.make(
        realname=name,
        mnemonic=mnemonic,
        body=body,
        type_key=type_key,
        desc=desc,
        tags=[characters.RawTag(*t) for t in tags])

    write_new_character(character, campaign)

    edit_files([character.file_path], settings = settings)

#######################
# Lint character files
#######################

@cli.command()
@click.option("--edit/--no-edit",
    default=False,
    help="Whether to open all character files with errors (default False)")
@pass_settings
def lint(settings, edit):
    """Check character files for errors

    This command only works within an existing campaign.
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    campaign.characters.refresh()

    error_characters = []
    for character in campaign.characters.all():
        linter = linters.CharacterLinter(character, campaign)
        linter.lint()
        if linter.errors:
            error_characters.append(character.file_path)
            echo(f"{character.name} has {len(linter.errors)} errors:")
            for error in linter.errors:
                echo(f"* {error.message}")

    if edit and error_characters:
        edit_files(error_characters, settings = settings)

#######################
# List character files
#######################

@cli.command()
@click.option("-f", "--format", "lang",
    default=None,
    help="The format to use.")
@click.option("-g", "--group-by", "group",
    default=None,
    multiple=True,
    help="Tags to group by. Additional groups will be nested.")
@click.option("-s", "--sort-by", "sort",
    default=None,
    multiple=True,
    help="Tags to sort by. Applied in order within the final group.")
@click.option("-h", "--header_level",
    default=None,
    type=click.IntRange(1, 6),
    help="The minimum header level to use.")
@click.option("-o", "--output",
    type=click.File('w'),
    required=True,
    help='Where to put the listing. Use "-" for STDOUT.')
@pass_settings
def list(settings, lang, group, sort, output, header_level):
    """Generate a public listing of characters

    This command only works within an existing campaign.

    All options default to getting their values from your settings. Use the keys under
    campaign.characters.listing to see and change these default values.
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    campaign.characters.refresh()

    lister = listers.CharacterLister(
        campaign.characters,
        lang=lang,
        group_by=group,
        sort_by=sort,
        base_header_level=header_level)

    if output.name != '<stdout>':
        with click.progressbar(length=campaign.characters.count) as bar:
            def progress():
                bar.update(1)

            lister.list(target=output, progress_callback=progress)
    else:
        lister.list(target=output)

#############################
# Reorganize character files
#############################

@cli.command()
@click.option("--keep-empty/--del-empty",
    default=True,
    help="Whether to keep empty directories after all files are moved.")
@click.option("--dryrun/--apply",
    default=True,
    help="Whether to show the changes that would be made, or actually make those changes")
@pass_settings
def reorg(settings, keep_empty, dryrun):
    """Reorganize character files

    This command only works within an existing campaign.

    As moving around a bunch of files can be disruptive, this command by default
    runs in "dryrun" mode, where the changes which would be made are displayed,
    but no files are actually moved. To apply changes, use the --apply flag.
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    # use campaign helper to handle the logic
    # need to call out any conflict warnings even with dryrun=False
