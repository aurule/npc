import click
from click import echo

from npc.util import ParseError
from npc_cli.presenters import tabularize, type_list, wrapped_paragraphs, tag_table_data
from npc_cli.helpers import cwd_campaign

from .main_group import cli, arg_settings, pass_settings

##########################
# Config description group
##########################

@cli.group()
def describe():
    """Show info about systems, types, or tags"""

###################
# Describe systems
###################

@describe.command()
@pass_settings
def systems(settings):
    """Show all configured game systems"""
    systems = [settings.get_system(key) for key in settings.get_system_keys()]
    system_headers = ["Name", "Key", "Description"]
    system_data = [[system.name, system.key, system.desc] for system in systems]
    echo(tabularize(system_data, headers = system_headers, title = "Configured Systems"))

    campaign = cwd_campaign(settings)
    if campaign:
        echo(f"\nCurrently using {campaign.system.name}")

##########################
# Describe system details
##########################

@describe.command()
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to show")
@pass_settings
def system(settings, system):
    """Show details about a single system"""
    campaign = cwd_campaign(settings)
    try:
        if system:
            game_system = settings.get_system(system)
        elif campaign:
            game_system = campaign.system
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    echo(f"=== {game_system.name} ===")
    echo(game_system.desc)
    for line in wrapped_paragraphs(game_system.doc):
        echo("")
        echo(line)
    if game_system.links:
        echo(f"\nRelevant Links:")
        for link in game_system.links:
            echo(f'* {link["label"]}: {link["url"]}')

###################
# Describe types
###################

@describe.command()
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@pass_settings
def types(settings, system):
    """Show all configured character types"""
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
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    chartype_headers = ["Name", "Key", "Description"]
    chartype_data = [[chartype.name, chartype.key, chartype.desc] for chartype in chartypes.values()]
    echo(tabularize(chartype_data, headers = chartype_headers, title = title))

########################
# Describe type details
########################

@describe.command()
@click.option("-s", "--system",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@click.option("-t", "--type", "type_",
    required=True,
    help="Character type to show")
@pass_settings
def type(settings, system, type_):
    """Show details about a single character type"""
    campaign = cwd_campaign(settings)
    try:
        if system:
            target = settings.get_system(system)
        elif campaign:
            target = campaign
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    if type_ not in target.types:
        raise click.BadParameter(f"'{type_}' is not one of {type_list(target.types)}", param_hint="'-t' / '--type'")
    chartype = target.get_type(type_)

    echo(f"Character Type: {chartype.name}")
    echo(f"ID: {chartype.key}")
    echo(f"File suffix: {chartype.default_sheet_suffix}")
    echo(f"Sheet template: {chartype.sheet_path}")
    echo("")
    echo(chartype.desc)

###################
# Describe tags
###################

@describe.command()
@click.option("-s", "--system", "system_key",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@click.option("-t", "--type", "type_", help="Only show valid tags for this character type")
@pass_settings
def tags(settings, system_key, type_):
    """Show all configured tags for this campaign

    Can show the tags available to all character types, or just the ones for a specific type.
    """
    campaign = cwd_campaign(settings)
    try:
        if system_key:
            target = settings.get_system(system_key)
            system = target
        elif campaign:
            target = campaign
            system = campaign.system
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    headers = ["Name", "Description"]
    if type_:
        if type_ not in target.types:
            raise click.BadParameter(f"'{type_}' is not one of {type_list(target.types)}", param_hint="'-t' / '--type'")

        title = f"Tags for {target.get_type(type_).name} in {target.name}"
        tags = target.type_tags(type_)
    else:
        title = f"Tags in {target.name}"
        tags = target.tags

    data = tag_table_data(tags)
    echo(tabularize(data, headers = headers, title = title))

#######################
# Describe tag details
#######################

@describe.command()
@click.option("-s", "--system", "system_key",
    type=click.Choice(arg_settings.get_system_keys(), case_sensitive=False),
    help="ID of the game system to use")
@click.option("-t", "--type", "type_",
    help="ID of the character type to use for finding the tag")
@click.option("-a", "--tag", "tag_name",
    required=True,
    help="Name of the tag to show")
@click.option("-c", "--context",
    help="Name of the tag's parent, if looking for a subtag")
@pass_settings
def tag(settings, system_key, type_, tag_name, context):
    """Show details for the named tag"""
    campaign = cwd_campaign(settings)
    try:
        if system_key:
            target = settings.get_system(system_key)
            system = target
        elif campaign:
            target = campaign
            system = campaign.system
        else:
            raise click.UsageError("Not a campaign, so the --system option must be provided")
    except ParseError as err:
        raise click.FileError(err.path, hint=err.strerror)

    headers = ["Name", "Description"]
    if type_:
        if type_ not in target.types:
            raise click.BadParameter(f"'{type_}' is not one of {type_list(target.types)}", param_hint="'-t' / '--type'")
        spec = target.get_type_tag(tag_name, type_)
    else:
        spec = target.get_tag(tag_name)

    if spec.needs_context:
        if not context:
            raise click.UsageError(f"Tag '{tag_name}' is a subtag, so the --context option must be provided")
        spec = spec.in_context(context)
        title = f"Tag: @{spec.name} (subtag of @{context})"
    else:
        title = f"Tag: @{spec.name}"

    echo(title)
    echo(spec.desc)
    for line in wrapped_paragraphs(spec.doc):
        echo("")
        echo(line)
