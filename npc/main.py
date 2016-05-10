#!/usr/bin/env python3.5

import re
import argparse
import json
import sys
from os import chdir, getcwd, path
from subprocess import run

# local packages
from . import commands, util

class Settings:
    """Load and store settings

    Default settings are loaded from support/settings-default.json in the
    install path.

    Do not access settings values directly. Use the get() method.
    """
    install_base = path.dirname(path.realpath(__file__))

    default_settings_path = path.join(install_base, 'support/settings-default.json')
    user_settings_path = path.expanduser('~/.config/npc/settings-user.json')
    campaign_settings_path = '.npc/settings-campaign.json'

    default_extra_paths = [user_settings_path, campaign_settings_path]

    def __init__(self, settings_path=default_settings_path, extra_paths=default_extra_paths):
        self.data = util.load_json(settings_path)

        for k, v in self.data['templates'].items():
            self.data['templates'][k] = path.join(self.install_base, v)
        for k, v in self.data['support'].items():
            self.data['support'][k] = path.join(self.install_base, v)

        for p in extra_paths:
            self.load_more(p)

    def load_more(self, settings_path):
        """Merge settings from a file

        Settings values from this file will override the defaults. Any errors
        while opening the file are suppressed and the file will simply not be
        loaded. In that case, existing values are left alone.
        """
        try:
            loaded = util.load_json(settings_path)
        except Exception as e:
            if hasattr(e, 'nicemsg'):
                sys.stderr.write(e.nicemsg)
            return

        def evaluate_paths(base, loaded, key):
            if key in loaded:
                loaded[key] = {k: path.join(absolute_path_base, path.expanduser(v)) for k, v in loaded[key].items()}

        # paths should be evaluated relative to the settings file in settings_path
        absolute_path_base = path.dirname(path.realpath(settings_path))
        evaluate_paths(absolute_path_base, loaded, 'support')
        evaluate_paths(absolute_path_base, loaded, 'templates')

        self.data = self._merge_settings(loaded, self.data)

    def _merge_settings(self, new_data, orig):
        dest = dict(orig)

        for k, v in new_data.items():
            if k in dest:
                if isinstance(dest[k], dict):
                    dest[k] = self._merge_settings(v, dest[k])
                else:
                    dest[k] = v
            else:
                dest[k] = v

        return dest

    def get_settings_path(self, settings_type):
        """Get a settings file path"""
        if settings_type == 'default':
            return self.default_settings_path

        if settings_type == 'user':
            return self.user_settings_path

        if settings_type == 'campaign':
            return self.campaign_settings_path

    def get(self, key):
        """Get the value of a settings key

        Use the period character to indicate a nested key.
        """
        key_parts = key.split('.')
        d = self.data
        for k in key_parts:
            try:
                d = d[k]
            except KeyError:
                return None
        return d

    def get_metadata(self, fmt):
        return {**self.get('additional_metadata.all'), **self.get('additional_metadata.%s' % fmt)}

def cli(argv):
    """Run the interface"""

    # load settings data and create parser
    prefs = Settings()
    parser = _make_parser(prefs)

    # Parse args
    args = parser.parse_args(argv)

    # change to the proper campaign directory if needed
    base = args.campaign
    if base == 'auto':
        base = _find_campaign_base()

    try:
        chdir(base)
    except OSError as e:
        print("{}: '{}'".format(e.strerror, base))
        return 4 # internal code for a filesystem error

    # run the command
    try:
        result = args.func(args, prefs)
    except AttributeError:
        parser.print_help()
        return 6

    # handle errors
    if not result.success:
        print(result.errmsg)
        return result.errcode

    # open the resulting files, if allowed
    if result.openable and not args.batch:
        run([prefs.get("editor")] + result.openable)

def _find_campaign_base():
    """Figure out the base campaign directory

    Walks up the directory tree until it finds the '.npc' campaign config
    directory, or hits the filesystem root. If the `.npc` directory is found, its
    parent is assumed to be the campaign's root directory. Otherwise, the
    current directory of the command invocation is used.
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

def _make_parser(prefs):
    # This parser stores options shared by all character creation commands. It is never exposed directly.
    character_parser = argparse.ArgumentParser(add_help=False)
    character_parser.add_argument('name', help="Character name", metavar='name')
    character_parser.add_argument('-g', '--group', default=[], nargs="*", help='Name of a group that counts the character as a member', metavar='group')
    character_parser.add_argument('--dead', default=False, const='', nargs='?', help='Mark that the character has died, with optional notes', metavar='notes')
    character_parser.add_argument('--foreign', default=False, help="Mark that the character is foreign to the main campaign setting, with optional notes on where they're from", metavar='location')

    # Parent parser for shared pathing options
    paths_parser = argparse.ArgumentParser(add_help=False)
    paths_parser.add_argument('--search', nargs="*", default=[prefs.get('paths.characters')], help="Paths to search. Individual files are added verbatim and directories are searched recursively.", metavar="PATH")
    paths_parser.add_argument('--ignore', nargs="*", default=[], help="Paths to skip when searching for character files", metavar="PATH")

    # This is the main parser which handles program-wide options. These should be kept sparse.
    parser = argparse.ArgumentParser(description = 'GM helper script to manage game files')
    parser.add_argument('-b', '--batch', action='store_true', default=False, help="Do not open any newly created files")
    parser.add_argument('--campaign', default='auto', help="Use the campaign files in a different directory", metavar='DIR')
    subparsers = parser.add_subparsers(title='Subcommands', description="Commands that can be run on the current campaign. See `%(prog)s <command> -h` to get help with individual commands.")

    # Subcommand to create the basic directories
    parser_init = subparsers.add_parser('init', help="Create the basic directory structure for campaign files")
    parser_init.add_argument('-t', '--types', action="store_true", default=False, help="Create directories for character types")
    parser_init.add_argument('-a', '--all', action="store_true", default=False, help="Create all optional directories")
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
    parser_changeling.set_defaults(func=commands.create_changeling)

    # Subcommand for linting characer files
    parser_lint = subparsers.add_parser('lint', parents=[paths_parser], help="Check the character files for minimum completeness")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="automatically fix certain problems")
    parser_lint.set_defaults(func=commands.lint)

    # Subcommand to list character data in multiple formats
    parser_list = subparsers.add_parser('list', parents=[paths_parser], help="Generate an NPC Listing")
    parser_list.add_argument('-t', '--format', choices=['markdown', 'md', 'json'], default=prefs.get('default_list_format'), help="Format to use for the listing. Defaults to 'md'")
    parser_list.add_argument('-m', '--metadata', nargs="?", const='default', default=False, help="Add metadata to the output. When the output format supports more than one metadata scheme, you can specify that scheme as well.")
    parser_list.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="File where the listing will be saved")
    parser_list.set_defaults(func=commands.list)

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
    parser_reorg.set_defaults(func=commands.reorg)

    # Open settings files
    parser_settings = subparsers.add_parser('settings', help="Open (and create if needed) a settings file")
    parser_settings.add_argument('location', choices=['user', 'campaign'], help="The settings file to load")
    parser_settings.add_argument('-d', '--defaults', action="store_true", default=False, help="Open the default settings file for easy reference")
    parser_settings.set_defaults(func=commands.settings)

    return parser
