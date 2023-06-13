import click
from click import echo

from npc import characters
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
