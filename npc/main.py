"""
Main entry point for NPC

Provides the cli method for interpreting commandline arguments.
"""

import argparse
from os import chdir, getcwd, path
from subprocess import run

# local packages
from . import commands, util, settings

def cli(argv):
    """
    Run the interface

    Args:
        argv (list): Arguments from the command invocation

    Returns:
        Return code indicating success or failure type. See `util.Result` for a
        list of return codes.
    """

    # create parser and parse args
    parser = _make_parser()
    args = parser.parse_args(argv)

    # change to the proper campaign directory if needed
    base = args.campaign
    if base == 'auto':
        base = find_campaign_root()

    try:
        chdir(base)
    except OSError as err:
        util.error("{}: '{}'".format(err.strerror, base))
        return 4 # internal code for a filesystem error

    # load settings data
    try:
        prefs = settings.InternalSettings(args.debug)
    except OSError as err:
        util.error(err.strerror + " ({})".format(prefs.get_settings_path('default')))
        return 4

    if not settings.lint_changeling_settings(prefs):
        return 5

    # show help when no input was given
    if not hasattr(args, 'func'):
        parser.print_help()
        return 0

    # get args as a dict
    full_args = vars(args)
    try:
        # load default character path if search field is at its default
        if full_args['search'] is None:
            full_args['search'] = [prefs.get('paths.characters')]
    except KeyError:
        pass

    # run the command
    try:
        if 'serialize' in full_args:
            serial_args = [full_args[k] for k in full_args['serialize']]
            for k in full_args['serialize']:
                full_args.pop(k)
        else:
            serial_args = []

        result = args.func(*serial_args, **full_args)
    except AttributeError as err:
        util.error(err)
        parser.print_help()
        return 6

    # handle errors
    if not result.success:
        util.error(result)
        return result.errcode

    # open the resulting files, if allowed
    if result.openable and not args.batch:
        run([prefs.get("editor")] + result.openable)

    return 0

def find_campaign_root():
    """
    Determine the base campaign directory

    Walks up the directory tree until it finds the '.npc' campaign config
    directory, or hits the filesystem root. If the `.npc` directory is found,
    its parent is assumed to be the campaign's root directory. Otherwise, the
    current directory of the command invocation is used.

    Returns:
        Directory path to the campaign.
    """
    current_dir = getcwd()
    base = current_dir
    old_base = ''
    while not path.isdir(path.join(base, '.npc')):
        old_base = base
        base = path.abspath(path.join(base, path.pardir))
        if old_base == base:
            return current_dir
    return base

def _make_parser():
    """
    Construct the arguments parser

    Returns:
        Complete argparser object
    """
    # This parser stores options shared by all character creation commands. It is never exposed directly.
    character_parser = argparse.ArgumentParser(add_help=False)
    character_parser.add_argument('name', help="Character name", metavar='name')
    character_parser.add_argument('-g', '--groups', default=None, nargs="*", help='Name of a group that counts the character as a member', metavar='group')
    character_parser.add_argument('--dead', default=False, const='', nargs='?', help='Mark that the character has died, with optional notes', metavar='notes')
    character_parser.add_argument('--foreign', default=False, help="Mark that the character is foreign to the main campaign setting, with optional notes on where they're from", metavar='location')
    character_parser.set_defaults(serialize=['name', 'ctype'])

    # Parent parser for shared pathing options
    paths_parser = argparse.ArgumentParser(add_help=False)
    paths_parser.add_argument('--search', nargs="*", default=None, help="Paths to search. Individual files are added verbatim and directories are searched recursively.", metavar="PATH")
    paths_parser.add_argument('--ignore', nargs="*", default=None, help="Paths to skip when searching for character files", metavar="PATH")
    paths_parser.set_defaults(serialize=['search'])

    # This is the main parser which handles program-wide options. These should be kept sparse.
    parser = argparse.ArgumentParser(description='GM helper script to manage game files')
    parser.add_argument('-b', '--batch', action='store_true', default=False, help="Do not open any newly created files")
    parser.add_argument('--campaign', default='auto', help="Use the campaign files in a different directory", metavar='DIR')
    parser.add_argument('--debug', action='store_true', default=False, help="Show all error messages, not just important ones")
    subparsers = parser.add_subparsers(title='Subcommands', description="Commands that can be run on the current campaign. See `%(prog)s <command> -h` to get help with individual commands.")

    # Subcommand to create the basic directories
    parser_init = subparsers.add_parser('init', help="Create the basic directory structure for campaign files")
    parser_init.add_argument('-t', '--types', action="store_true", default=False, help="Create directories for character types", dest="create_types")
    parser_init.add_argument('-a', '--all', action="store_true", default=False, help="Create all optional directories", dest="create_all")
    parser_init.set_defaults(func=commands.init)

    # Session subcommand
    parser_session = subparsers.add_parser('session', help="Create files for a new game session")
    parser_session.set_defaults(func=commands.session)

    # Create generic character
    parser_generic = subparsers.add_parser('generic', aliases=['g'], parents=[character_parser], help="Create a new character using the named template")
    parser_generic.add_argument('ctype', metavar='template', help="Template to use. Must be configured in settings")
    parser_generic.set_defaults(func=commands.create_simple)

    # These parsers are just named subcommand entry points to create simple characters
    parser_human = subparsers.add_parser('human', aliases=['h'], parents=[character_parser], help="Create a new human character. Alias for `npc generic human`")
    parser_human.set_defaults(func=commands.create_simple, ctype="human")
    parser_fetch = subparsers.add_parser('fetch', parents=[character_parser], help="Create a new fetch character. Alias for `npc generic fetch`")
    parser_fetch.set_defaults(func=commands.create_simple, ctype="fetch")
    parser_goblin = subparsers.add_parser('goblin', parents=[character_parser], help="Create a new goblin character. Alias for `npc generic goblin`")
    parser_goblin.set_defaults(func=commands.create_simple, ctype="goblin")

    # Subcommand for making changelings, with their unique options
    parser_changeling = subparsers.add_parser('changeling', aliases=['c'], parents=[character_parser], help="Create a new changeling character")
    parser_changeling.add_argument('seeming', help="character's Seeming", metavar='seeming')
    parser_changeling.add_argument('kith', help="character's Kith", metavar='kith')
    parser_changeling.add_argument('-c', '--court', help="the character's Court", metavar='court')
    parser_changeling.add_argument('-m', '--motley', help="the character's Motley", metavar='motley')
    parser_changeling.set_defaults(func=commands.create_changeling, serialize=['name', 'seeming', 'kith'])

    # Subcommand for linting characer files
    parser_lint = subparsers.add_parser('lint', parents=[paths_parser], help="Check the character files for minimum completeness")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="automatically fix certain problems")
    parser_lint.set_defaults(func=commands.lint)

    # Subcommand to list character data in multiple formats
    parser_list = subparsers.add_parser('list', parents=[paths_parser], help="Generate an NPC Listing")
    parser_list.add_argument('-t', '--format', choices=['markdown', 'md', 'json', 'htm', 'html'], default='default', help="Format to use for the listing. Defaults to 'md'", dest="fmt")
    parser_list.add_argument('-m', '--metadata', nargs="?", const='default', default=False, help="Add metadata to the output. If the output format supports more than one metadata format, you can specify that format as well.")
    parser_list.add_argument('--title', help="Title to show in the metadata. Overrides the title in settings.", metavar="TITLE")
    parser_list.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_list.set_defaults(func=commands.listing)

    # Dump raw character data
    parser_dump = subparsers.add_parser('dump', parents=[paths_parser], help="Export raw json data of all characters")
    parser_dump.add_argument('-s', '--sort', action="store_true", default=False, help="Sort the characters")
    parser_dump.add_argument('-m', '--metadata', action="store_true", default=False, help="Add metadata to the output.")
    parser_dump.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_dump.set_defaults(func=commands.dump)

    # Reorganize character files subcommand
    parser_reorg = subparsers.add_parser('reorg', parents=[paths_parser], help="Move character files to the most appropriate directories")
    parser_reorg.add_argument('-p', '--purge', action="store_true", default=False, help="After moving all files, remove any empty directories within the base characters path")
    parser_reorg.add_argument('-v', '--verbose', action="store_true", default=False, help="Show the changes that are made")
    parser_reorg.add_argument('-d', '--dry-run', action="store_true", default=False, help="Show the changes that would be made, but don't change anything", dest="dry")
    parser_reorg.set_defaults(func=commands.reorg)

    # Open settings files
    parser_settings = subparsers.add_parser('settings', help="Open (and create if needed) a settings file")
    parser_settings.add_argument('location', choices=['user', 'campaign'], help="The settings file to load")
    parser_settings.add_argument('-t', '--type', choices=['base', 'changeling'], help="Open a type-specific settings file", metavar='type', dest='settings_type')
    parser_settings.add_argument('-d', '--defaults', action="store_true", default=False, help="Open the default settings file for easy reference", dest='show_defaults')
    parser_settings.set_defaults(func=commands.open_settings, serialize=['location'])

    return parser
