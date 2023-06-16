import click
from click import echo, BadParameter

from npc import characters, linters
from npc.reporters import tag_reporter
from npc.util import edit_files
from npc_cli.presenters import type_list, tabularize
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


##########################
# Config reports group
##########################

@cli.group()
def report():
    """Show stats about the characters in this campaign"""


#######################
# Show tag stastistics
#######################

@report.command()
@click.option("-t", "--tag", "tag_name",
    help="Tag to analyze")
@click.option("-c", "--context",
    help="Parent context if tag is a subtag. Use '*' to disregard parent.")
@pass_settings
def values(settings, tag_name, context):
    """Show a how many times each unique value appears for the given tag

    This command only works within an existing campaign

    The '--context' option is only needed if '--tag' is a subtag like role.
    """
    campaign = cwd_campaign(settings)
    if campaign is None:
        raise CampaignNotFoundException

    campaign.characters.refresh()

    spec = campaign.get_tag(tag_name)
    if spec.needs_context and context != "*":
        valid_contexts = list(spec.contexts.keys()) + ["*"]
        if (not context) or (context not in valid_contexts):
            raise click.BadParameter(f"{tag_name} tag requires context to be one of {valid_contexts}", param_hint=['-c', '--context'])
        data = tag_reporter.subtag_value_counts_report(tag_name, context)
        prefix: str = f"@{tag_name} ({context})"
    else:
        data = tag_reporter.value_counts_report(tag_name)
        prefix: str = f"@{tag_name} tag"

    title: str = f"{prefix} values report"
    headers = ("Value", "Count")
    echo(tabularize(data, headers=headers, title=title))
