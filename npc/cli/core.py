"""
Main entry point for NPC

Provides the cli method for interpreting commandline arguments.
"""

import argparse
import sys
from os import chdir, getcwd, path

# local packages
from npc import util, settings
from npc.__version__ import __version__
from . import progress_bar, commands

def start(argv=None):
    """
    Run the command-line interface

    Args:
        argv (list): Arguments from the command invocation. When running from
            code, this should just include the arguments you want to use, not
            the name of the script itself. When left blank, sys.argv will be
            used instead after chopping off the first argument.

    Returns:
        Integer code of zero for success or non-zero for failure.
    """

    # create parser and parse args
    parser = _make_parser()
    if not argv:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)

    # change to the proper campaign directory if needed
    base = args.campaign
    if base == 'auto':
        base = util.find_campaign_root()

    try:
        chdir(base)
    except OSError as err:
        util.error("{}: '{}'".format(err.strerror, base))
        return 4

    # load settings data
    try:
        prefs = settings.Settings(args.debug)
    except OSError as err:
        util.error(err.strerror)
        return 4

    changeling_errors = settings.lint_changeling_settings(prefs)
    if changeling_errors:
        print("\n".join(changeling_errors))
        return 5

    # show help when no input was given
    if not hasattr(args, 'func'):
        parser.print_help()
        return 0

    # get args as a dict
    full_args = vars(args)
    full_args['prefs'] = prefs

    # load default character path if search field is at its default
    if full_args.get('search') is None:
        full_args['search'] = [prefs.get('paths.required.characters')]

    # run the command
    try:
        result = args.func(full_args)
    except AttributeError as err:
        if args.debug:
            raise
        util.error(err)
        return 6

    # handle errors
    if not result.success:
        util.error(result)
        return result.errcode

    if not args.batch:
        # print any messages that were returned
        if result.printables:
            print("\n".join(result.printables))

        # open the resulting files, if allowed
        if result.openable:
            util.open_files(*result.openable, prefs=prefs)

    return 0

def _make_parser():
    """
    Construct the arguments parser

    Returns:
        Complete argparser object
    """
    # This parser stores options shared by all character creation commands. It
    # is never exposed directly.
    character_parser = argparse.ArgumentParser(add_help=False)
    character_parser.add_argument('-g', '--groups', default=None, nargs="*", help='Name of a group that counts the character as a member', metavar='group')
    character_parser.add_argument('--dead', default=False, const='', nargs='?', help='Mark that the character has died, with optional notes', metavar='notes')
    character_parser.add_argument('--foreign', default=False, const='', nargs='?', help="Mark that the character is foreign to the main campaign setting, with optional notes on where they're from", metavar='place')
    character_parser.add_argument('--location', default=False, help="Where the character is located within the main setting", metavar='place')

    # Parent parser for shared pathing options
    paths_parser = argparse.ArgumentParser(add_help=False)
    paths_parser.add_argument('--search', nargs="*", default=None, help="Paths to search. Individual files are added verbatim and directories are searched recursively.", metavar="PATH")
    paths_parser.add_argument('--ignore', nargs="*", default=None, help="Paths to skip when searching for character files", metavar="PATH")

    common_options = argparse.ArgumentParser(add_help=False)
    common_options.add_argument('-b', '--batch', action='store_true', default=False, help="Do not print any messages or open any files in the editor")
    common_options.add_argument('--debug', action='store_true', default=False, help="Show all error messages, not just important ones")

    # This is the main parser which handles program-wide options. These should
    # be kept sparse.
    parser = argparse.ArgumentParser(description='GM helper script to manage game files', prog='npc')
    parser.add_argument('--campaign', default='auto', help="Use the campaign files in a different directory", metavar='DIR')
    parser.add_argument('--version', action='version', version=__version__)
    parser.set_defaults(debug=False, batch=False)
    subparsers = parser.add_subparsers(title='Subcommands', description="Commands that can be run on the current campaign. See `%(prog)s <command> -h` to get help with individual commands.")

    # Subcommand to create the basic directories
    parser_init = subparsers.add_parser('init', parents=[common_options], help="Create the basic directory structure for campaign files")
    parser_init.add_argument('-n', '--name', default=None, help="Name of the campaign. Defaults to the name of the current directory.", dest="campaign_name")
    parser_init.add_argument('-t', '--types', action="store_true", default=False, help="Create directories for all character types", dest="create_types")
    parser_init.add_argument('-a', '--all', action="store_true", default=False, help="Create all optional directories", dest="create_all")
    parser_init.add_argument('-v', '--verbose', action="store_true", default=False, help="Show the changes that are made")
    parser_init.add_argument('--dryrun', action="store_true", default=False, help="Show what would be created, but do not actually change anything")
    parser_init.set_defaults(func=commands.init)

    # Session subcommand
    parser_session = subparsers.add_parser('session', parents=[common_options], help="Create files for a new game session")
    parser_session.set_defaults(func=commands.session)

    # Latest plot/session command
    parser_latest = subparsers.add_parser('latest', parents=[common_options], help="Get the latest plot and/or session files")
    parser_latest.add_argument('thingtype', nargs='?', default='both', choices=['both', 'session', 'plot'], help="Type of file to open. One of 'plot', 'session', or 'both'. Defualts to 'both'.")
    parser_latest.set_defaults(func=commands.latest)

    # Create generic character
    parser_generic = subparsers.add_parser('new', parents=[common_options, character_parser], help="Create a new character from the named template")
    parser_generic.add_argument('ctype', metavar='template', help="Template to use. Must be configured in settings")
    parser_generic.add_argument('name', help="Character name", metavar='name')
    parser_generic.set_defaults(func=commands.create_standard)

    # These parsers are just named subcommand entry points to create simple
    # characters
    parser_human = subparsers.add_parser('human', aliases=['h'], parents=[common_options, character_parser], help="Create a new human character. Alias for `npc new human`")
    parser_human.add_argument('name', help="Character name", metavar='name')
    parser_human.set_defaults(func=commands.create_standard, ctype="human")

    # Subcommand for making changelings, with their unique options
    parser_changeling = subparsers.add_parser('changeling', aliases=['c'], parents=[common_options, character_parser], help="Create a new changeling character")
    parser_changeling.add_argument('name', help="Character name", metavar='name')
    parser_changeling.add_argument('seeming', help="The character's Seeming", metavar='seeming')
    parser_changeling.add_argument('kith', help="The character's Kith", metavar='kith')
    parser_changeling.add_argument('-c', '--court', help="The character's Court", metavar='court')
    parser_changeling.add_argument('-m', '--motley', help="The character's Motley", metavar='motley')
    parser_changeling.set_defaults(func=commands.create_changeling)

    # Subcommand for linting characer files
    parser_lint = subparsers.add_parser('lint', parents=[common_options, paths_parser], help="Check the character files for minimum completeness")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="Automatically fix certain problems")
    parser_lint.add_argument('-p', '--report', action='store_true', default=False, help="Display a report of problems, but do not open the related files")
    parser_lint.add_argument('--strict', action='store_true', default=False, help="Include all optional and non-critical errors")
    parser_lint.set_defaults(func=commands.lint)

    # Subcommand to list character data in multiple formats
    parser_list = subparsers.add_parser('list', parents=[common_options, paths_parser], help="Generate an NPC Listing")
    parser_list.add_argument('-t', '--format', choices=['markdown', 'md', 'json', 'htm', 'html'], default='default', help="Format to use for the listing. Defaults to the list format in settings", dest="fmt")
    parser_list.add_argument('-m', '--metadata', nargs="?", const='default', default=False, help="Add metadata to the output. If the output format supports more than one metadata format, you can specify that format as well.")
    parser_list.add_argument('--title', help="Title to show in the metadata. Overrides the title from settings.", metavar="TITLE")
    parser_list.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_list.add_argument('--sort', dest='sort_by', default=None, help="The sort order for characters. Separate multiple tags with a comma. Defaults to the settings value 'listing.sort_by'.")
    parser_list.add_argument('--no_sort', action='store_false', dest='do_sort', help="Do not sort characters at all")
    parser_list.set_defaults(func=commands.make_list, progress=_update_progress_bar)

    # Dump raw character data
    parser_dump = subparsers.add_parser('dump', parents=[common_options, paths_parser], help="Export raw json data of all characters")
    parser_dump.add_argument('-s', '--sort', action="store_true", default=False, help="Sort the characters")
    parser_dump.add_argument('-m', '--metadata', action="store_true", default=False, help="Add metadata to the output.")
    parser_dump.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_dump.set_defaults(func=commands.dump)

    # Reorganize character files subcommand
    parser_reorg = subparsers.add_parser('reorg', parents=[common_options, paths_parser], help="Move character files to the most appropriate directories. By default, shows changes that would be made, but does not move anything. Use the --commit option once you're satisfied with where the files will end up.")
    parser_reorg.add_argument('-p', '--purge', action="store_true", default=False, help="After moving all files, remove any empty directories within the base characters path")
    parser_reorg.add_argument('-v', '--verbose', action="store_true", default=False, help="Show changes as they are made")
    parser_reorg.add_argument('--commit', action="store_true", default=False, help="Move the files around")
    parser_reorg.set_defaults(func=commands.reorg)

    # Open settings files
    parser_settings = subparsers.add_parser('settings', parents=[common_options], help="Open (and create if needed) a settings file")
    parser_settings.add_argument('location', choices=['user', 'campaign'], help="The settings file to load")
    parser_settings.add_argument('-t', '--type', choices=['base', 'changeling'], help="Open a type-specific settings file", metavar='type', dest='settings_type')
    parser_settings.add_argument('-d', '--defaults', action="store_true", default=False, help="Open the default settings file for easy reference", dest='show_defaults')
    parser_settings.set_defaults(func=commands.open_settings)

    # Report on character tags
    parser_report = subparsers.add_parser('report', parents=[common_options, paths_parser], help="Create a report of the values for one or more tags")
    parser_report.add_argument('tags', nargs="+", help="Tag names to analyze")
    parser_report.add_argument('-t', '--format', choices=['json', 'htm', 'html', 'md', 'markdown'], default='default', help="Format to use for the tables. Defaults to the table format in settings", dest="fmt")
    parser_report.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_report.set_defaults(func=commands.report)

    # Find characters by tag contents
    parser_find = subparsers.add_parser('find', parents=[common_options, paths_parser], help="Find characters by their tags")
    parser_find.add_argument('rules', nargs="+", help="Rules to search by. Format for each is tag:text. Negate with tag~:text.")
    parser_find.add_argument('-d', '--dryrun', action="store_true", default=False, help="Show the files that would be opened, but don't open anything", dest="dryrun")
    parser_find.set_defaults(func=commands.find)

    return parser

def _update_progress_bar(index, total):
    """Update the textual progressbar"""
    progress_bar.bar(index, total, prefix='Generating:', length=50)
