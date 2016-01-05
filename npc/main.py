#!/usr/bin/env python3.5

import re
import argparse
import json
import sys
import errno
from contextlib import contextmanager
from datetime import datetime
from os import path, walk, makedirs, rmdir, scandir, chdir, getcwd
from shutil import copy as shcopy, move as shmove
from subprocess import run

# local packages
from . import formatters, linters, parser

class Result:
    """Data about the result of a subcommand

    Attributes:
    * success   boolean Whether the subcommand ran correctly
    * openable  list    Paths to files which were changed by or are relevant to
                        the subcommand
    * errcode   integer Error code indicating the type of error encountered
    * errmsg    string  Human-readable error message. Will be displayed to the
                        user
    """
    def __init__(self, success, openable = None, errcode = 0, errmsg = ''):
        super(Result, self).__init__()
        self.success = success
        self.openable = openable
        self.errcode = errcode
        # Error codes:
        # 0. Everything's fine
        # 1. Tried to create a file that already exists
        # 2. Latest plot and session files have different numbers
        # 3. Feature is not yet implemented
        # 4. Filesystem error
        # 5. Unrecognized format
        # 6. Invalid option
        # 7. Unrecognized template
        self.errmsg = errmsg

def _load_json(filename):
    """ Parse a JSON file
        First remove all comments, then use the standard json package

        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    with open(filename) as f:
        content = ''.join(f.readlines())

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        # Return parsed json
        return json.loads(content)

class Settings:
    """Load and store settings

    Default settings are loaded from support/settings-default.json in the
    install path.

    Do not access settings values directly. Use the get() method.
    """
    install_base = path.dirname(path.realpath(__file__))
    path_default = path.join(install_base, 'support/settings-default.json')
    extra_paths = [
        path.expanduser('~/.config/npc/settings-user.json'),
        '.npc/settings-campaign.json'
    ]

    def __init__(self, settings_path = path_default):
        self.data = _load_json(settings_path)
        for k, v in self.data['templates'].items():
            self.data['templates'][k] = path.join(self.install_base, v)
        for k, v in self.data['support'].items():
            self.data['support'][k] = path.join(self.install_base, v)

        for p in self.extra_paths:
            self.load_more(p)

    def load_more(self, settings_path):
        """Merge settings from a file

        Settings values from this file will override the defaults. Any errors
        while opening the file are suppressed and the file will simply not be
        loaded.
        """
        try:
            loaded = _load_json(settings_path)
        except:
            return

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
            return self.path_default

        if settings_type == 'user':
            return self.extra_paths[0]

        if settings_type == 'campaign':
            return self.extra_paths[1]

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

def run(argv):
    """Run the interface"""

    # load settings data
    prefs = Settings()

    # This parser stores options shared by all character creation commands. It is never exposed directly.
    character_parser = argparse.ArgumentParser(add_help=False)
    character_parser.add_argument('name', help="character's name", metavar='name')
    character_parser.add_argument('-g', '--group', default=[], nargs="*", help='name of a group that counts the character as a member', metavar='group')

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
    parser_init = subparsers.add_parser('init', help="Set up the basic directory structure for campaign files")
    parser_init.add_argument('-t', '--types', action="store_true", default=False, help="Create directories for character types")
    parser_init.add_argument('-a', '--all', action="store_true", default=False, help="Create all optional directories")
    parser_init.set_defaults(func=do_init)

    # Session subcommand
    parser_session = subparsers.add_parser('session', aliases=['s'], help="Create files for a new game session")
    parser_session.set_defaults(func=do_session)

    parser_generic = subparsers.add_parser('generic', aliases=['g'], parents=[character_parser], help="Create a new character using the named template")
    parser_generic.add_argument('ctype', metavar='template', help="Template to use. Must be configured in settings")
    parser_generic.set_defaults(func=create_simple)

    # These parsers are just named subcommand entry points to create simple characters
    parser_human = subparsers.add_parser('human', aliases=['h'], parents=[character_parser], help="Create a new human character")
    parser_human.set_defaults(func=create_simple, ctype="human")
    parser_fetch = subparsers.add_parser('fetch', aliases=['f'], parents=[character_parser], help="Create a new fetch character")
    parser_fetch.set_defaults(func=create_simple, ctype="fetch")
    parser_goblin = subparsers.add_parser('goblin', parents=[character_parser], help="Create a new goblin character")
    parser_goblin.set_defaults(func=create_simple, ctype="goblin")

    # Subcommand for making changelings, with their unique options
    parser_changeling = subparsers.add_parser('changeling', aliases=['c'], parents=[character_parser], help="Create a new changeling character")
    parser_changeling.set_defaults(func=create_changeling)
    parser_changeling.add_argument('seeming', help="character's Seeming", metavar='seeming')
    parser_changeling.add_argument('kith', help="character's Kith", metavar='kith')
    parser_changeling.add_argument('-c', '--court', help="the character's Court", metavar='court')
    parser_changeling.add_argument('-m', '--motley', help="the character's Motley", metavar='motley')

    # Subcommand for linting characer files
    parser_lint = subparsers.add_parser('lint', parents=[paths_parser], help="Check the character files for minimum completeness.")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="automatically fix certain problems")
    parser_lint.set_defaults(func=do_lint)

    # Subcommand to list character data in multiple formats
    parser_webpage = subparsers.add_parser('list', aliases=['l'], parents=[paths_parser], help="Generate an NPC Listing")
    parser_webpage.add_argument('-t', '--format', choices=['markdown', 'md', 'json'], default=prefs.get('default_list_format'), help="Format to use for the listing. Defaults to 'md'")
    parser_webpage.add_argument('-m', '--metadata', nargs="?", const='default', default=False, help="Add metadata to the output. When the output format supports more than one metadata scheme, you can specify that scheme as well.")
    parser_webpage.add_argument('-o', '--outfile', nargs="?", const='-', default=None, help="file where the listing will be saved")
    parser_webpage.set_defaults(func=do_list)

    # Reorganize character files subcommand
    parser_reorg = subparsers.add_parser('reorg', parents=[paths_parser], help="Move character files to the most appropriate directories")
    parser_reorg.add_argument('-p', '--purge', action="store_true", default=False, help="After moving all files, remove any empty directories within the base characters path")
    parser_reorg.add_argument('-v', '--verbose', action="store_true", default=False, help="Show the changes that are made")
    parser_reorg.set_defaults(func=do_reorg)

    # Open settings files
    parser_settings = subparsers.add_parser('settings', help="Open (and create if needed) a settings file")
    parser_settings.add_argument('location', choices=['user', 'campaign'], help="The settings file to load")
    parser_settings.add_argument('-d', '--defaults', action="store_true", default=False, help="Open the default settings for reference")
    parser_settings.set_defaults(func=do_settings)

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
    directory, or hits the filesystem root.
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

def create_changeling(args, prefs):
    """Create a Changeling character

    Arguments:
    * args - object containing runtime data. Must contain the following
             attributes:
        + name              string  Base file name
        + seeming           string  Name of the character's Seeming. Added to
                                    the file with notes.
        + kith              string  Name of the character's Kith. Added to the
                                    file with notes.
        + court (optional)  string  Name of the character's Court. Used to
                                    derive path.
        + motley (optional) string  Name of the character's Motley.
        + group (optional)  list    One or more names of groups the character
                                    belongs to. Used to derive path.
    * prefs - Settings object
    """
    changeling_bonuses = prefs.get('support.changeling-sk')
    seeming_re = re.compile(
        '^(\s+)seeming(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        '^(\s+)kith(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )

    # Derive the path for the new file
    target_path = _add_path_if_exists(prefs.get('paths.characters'), prefs.get('type_paths.%s' % 'changeling'))
    if args.court:
        target_path = _add_path_if_exists(target_path, args.court.title())
    else:
        target_path = _add_path_if_exists(target_path, 'Courtless')

    for group_name in args.group:
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    # Create tags
    seeming_name = args.seeming.title()
    kith_name = args.kith.title()
    tags = ['@changeling %s %s' % (seeming_name, kith_name)]
    if args.motley:
        tags.append('@motley %s' % args.motley)
    if args.court:
        tags.append('@court %s' % args.court.title())
    tags.extend(["@group %s" % g for g in args.group])

    header = "\n".join(tags) + '\n\n'

    # Copy template data
    try:
        with open(prefs.get('templates.changeling'), 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % prefs.get('templates.changeling'), errcode=4)

    # insert seeming and kith in the advantages block
    try:
        sk = _load_json(changeling_bonuses)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % changeling_bonuses, errcode=4)
    if args.seeming.lower() in sk['blessing']:
        seeming_notes = "%s; %s" % (sk['blessing'][args.seeming.lower()], sk['curse'][args.seeming.lower()])
        data = seeming_re.sub(
            '\g<1>Seeming\g<2>%s (%s)' % (seeming_name, seeming_notes),
            data
        )
    if args.kith.lower() in sk['blessing']:
        kith_notes = sk['blessing'][args.kith.lower()]
        data = kith_re.sub(
            '\g<1>Kith\g<2>%s (%s)' % (kith_name, kith_notes),
            data
        )

    # Save the new character
    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def create_simple(args, prefs):
    """Create a character without extra processing

    Simple characters don't have any unique tags or file annotations. Everything
    is based on their type.

    Arguments:
    * args          object  Object with runtime data. Must contain the following
                            attributes:
        + name              string  Base file name
        + group (optional)  list    One or more names of groups the character
                                    belongs to. Used to derive path for the file.
    """
    ctype = args.ctype
    if ctype not in prefs.get('templates'):
        return Result(False, errmsg="Unrecognized template '%s'" % ctype, errcode=7)

    # Derive destination path
    target_path = _add_path_if_exists(prefs.get('paths.characters'), prefs.get('type_paths.%s' % ctype))
    for group_name in args.group:
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    # Add tags
    typetag = ctype.title()
    tags = ['@type %s' % typetag] + ["@group %s" % g for g in args.group]
    header = "\n".join(tags) + '\n\n'

    # Copy template
    template = prefs.get('templates.%s' % ctype)
    try:
        with open(template, 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % template, errcode=4)

    # Write the new file
    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def _add_path_if_exists(base, potential):
    """Add a directory to the base path if that directory exists"""
    test_path = path.join(base, potential)
    if path.exists(test_path):
        return test_path
    return base

def do_session(args, prefs):
    """Creates the files for a new game session

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log.
    """
    plot_re = re.compile('^plot (\d+)$')
    session_re = re.compile('^session (\d+)$')

    # find latest plot file and its number
    plot_files = [f.name for f in scandir(prefs.get('paths.plot')) if f.is_file() and plot_re.match(path.splitext(f.name)[0])]
    latest_plot = max(plot_files, key=lambda plot_files:re.split(r"\s", plot_files)[1])
    (latest_plot_name, latest_plot_ext) = path.splitext(latest_plot)
    plot_match = plot_re.match(latest_plot_name)
    plot_number = int(plot_match.group(1))

    # find latest session log and its number
    session_files = [f.name for f in scandir(prefs.get('paths.session')) if f.is_file() and session_re.match(path.splitext(f.name)[0])]
    latest_session = max(session_files, key=lambda session_files:re.split(r"\s", session_files)[1])
    (latest_session_name, latest_session_ext) = path.splitext(latest_session)
    session_match = session_re.match(latest_session_name)
    session_number = int(session_match.group(1))

    if plot_number != session_number:
        return Result(False, errmsg="Cannot create new plot and session files: latest files have different numbers (plot %i, session %i)" % (plot_number, session_number), errcode=2)

    new_number = plot_number + 1

    # copy old plot
    old_plot_path = path.join(prefs.get('paths.plot'), latest_plot)
    new_plot_path = path.join(prefs.get('paths.plot'), ("plot %i" % new_number) + latest_plot_ext)
    shcopy(old_plot_path, new_plot_path)

    # create new session log
    old_session_path = path.join(prefs.get('paths.session'), latest_session)
    new_session_path = path.join(prefs.get('paths.session'), ("session %i" % new_number) + latest_session_ext)
    shcopy(prefs.get('templates.session'), new_session_path)

    return Result(True, openable=[new_session_path, new_plot_path, old_plot_path, old_session_path])

def do_reorg(args, prefs):
    base_path = prefs.get('paths.characters')
    characters = parser.get_characters(args.search, args.ignore)
    for c in characters:
        new_path = create_path_from_character(c, base_path, prefs)
        if new_path != path.dirname(c['path']):
            if args.verbose:
                print("Moving {} to {}".format(c['path'], new_path))
            shmove(c['path'], new_path)

    if args.purge:
        for dirpath, dirnames, files in walk(base_path):
            try:
                rmdir(dirpath)
                if args.verbose:
                    print("Removing empty directory {}".format(dirpath))
            except OSError as e:
                if e.errno == errno.ENOTEMPTY:
                    continue
                else:
                    raise

    return Result(True)

def create_path_from_character(c, target_path, prefs):
    # add type-based directory if we can
    if 'type' in c:
        ctype = c['type'][0].lower()
        target_path = _add_path_if_exists(target_path, prefs.get('type_paths.%s' % ctype))
    else:
        ctype = 'none'

    # handle type-specific considerations
    if ctype == 'changeling':
        # changelings use court first, then groups
        if 'court' in c:
            for court_name in c['court']:
                target_path = _add_path_if_exists(target_path, court_name)
        else:
            target_path = _add_path_if_exists(target_path, 'Courtless')

    # everyone uses groups in their path
    if 'group' in c:
        for group_name in c['group']:
            target_path = _add_path_if_exists(target_path, group_name)

    return target_path

def do_list(args, prefs):
    """Generate a list of NPCs

    Arguments:
    * args - object containing runtime data. Must contain the following:
        + format    string      Format of the output. Supported types are
                                markdown (md), and json.
        + metadata  None|string Optional flag to include metadata in the output.
                                Additionally, the metadata format can be
                                specified for some output formats. The markdown
                                format supports adding either mmd
                                (MultiMarkdown) or yfm/yaml (Yaml Front Matter)
                                metadata.
        + outfile   string      Optional path to a file to hold the generated
                                listing. If omitted, the data will be printed to
                                stdout.
    * prefs - Settings object
    """
    characters = _sort_chars(parser.get_characters(args.search, args.ignore))

    out_type = args.format.lower()

    data = ''
    if out_type in ('md', 'markdown'):
        # ensure 'default' gets replaced with the right default metadata format
        metadata_type = args.metadata
        if metadata_type == 'default':
            metadata_type = prefs.get('metadata_format.markdown')

        # call out to get the markdown
        with _smart_open(args.outfile) as f:
            meta = prefs.get_metadata('markdown')
            formatters.markdown.dump(characters, f, metadata_type, meta)
    elif out_type == 'json':
        # make some json
        if args.metadata:
            base_meta = {
                'meta': True,
                'title': 'NPC Listing',
                'created': datetime.now().isoformat()
            }
            meta = {**base_meta, **prefs.get_metadata('json')}
            characters = [meta] + characters

        with _smart_open(args.outfile) as f:
            json.dump(characters, f)

    else:
        return Result(False, errmsg="Cannot create output of format '%s'", errcode=5)

    openable = None
    if args.outfile and args.outfile != '-':
        openable = [args.outfile]

    return Result(True, openable=openable)

def _sort_chars(characters):
    """Sort a list of character dicts.

    In the future, this is where different sort methods will be handled.
    """
    return sorted(characters, key=lambda c: c['name'][0].split(' ')[-1])

@contextmanager
def _smart_open(filename=None):
    """Open a named file or stdout as appropriate

    When filename is None or the dash character ('-'), this method will yield
    sys.stdout. When filename is a path, it will open the file for writing.
    Either way, a file-like object is returned.

    This method is designed to be used in a `with` block.
    """
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def do_lint(args, prefs):
    """Check character files for completeness and correctness

    Arguments:
    * args  object  Object with runtime data. Must contain the following
                    attributes:
        + fix   boolean     Whether to automatically fix errors when possible
    * prefs object  Settings object

    This method checks that every character file has a few required tags, and
    applies extra checking for some character types.

    Required tags:
    * description - Not a tag, but the file must have description content
    * @type - Character type

    Extra checks for Changelings:
    * @seeming tag is present and valid
    * @kith tag is present and valid
    """
    characters = parser.get_characters(args.search, args.ignore)
    changeling_bonuses = path.join(prefs.install_base, 'support/seeming-kith.json')
    sk = None

    openable = []
    for c in characters:
        problems = []
        fixes = []
        data = None

        # Check description
        if not c['description'].strip():
            problems.append("Missing description")

        # Check type tag
        if not 'type' in c:
            problems.append("Missing @type tag")
        else:
            # Do additional processing based on reported type
            types = [t.lower() for t in c['type']]
            if 'changeling' in types:
                # lazily load and cache our seeming and kith data
                if not sk:
                    try:
                        sk = _load_json(changeling_bonuses)
                    except IOError as e:
                        return Result(False, errmsg=e.strerror + " (%s)" % changeling_bonuses, errcode=4)

                # find (and fix) changeling-specific problems in the body of the sheet
                problems.extend(linters.changeling.lint(c, args.fix, sk=sk))

        # Report problems on one line if possible, or as a block if there's more than one
        if len(problems):
            openable.append(c['path'])
            if len(problems) > 1:
                print("File '%s':" % c['path'])
                for p in problems:
                    print("    %s" % p)
            else:
                print("%s in '%s'" % (problems[0], c['path']))

    return Result(True, openable)

def do_init(args, prefs):
    """Create the basic directories for a campaign

    This will create the directories this tool expects to find within a
    campaign. Other directories are left to the user.
    """
    for k, p in prefs.get('paths').items():
        makedirs(p, mode=0o775, exist_ok=True)
    makedirs('.npc', mode=0o775, exist_ok=True)

    if args.types or args.all:
        cbase = prefs.get('paths.characters')
        for k, p in prefs.get('type_paths').items():
            makedirs(path.join(cbase, p), mode=0o775, exist_ok=True)

    return Result(True)

def do_settings(args, prefs):
    """Open the named settings file"""
    target_path = prefs.get_settings_path(args.location)
    if not path.exists(target_path):
        dirname = path.dirname(target_path)
        makedirs(dirname, mode=0o775, exist_ok=True)
        open(target_path, 'a').close()

    if args.defaults:
        openable = [prefs.get_settings_path('default'), target_path]
    else:
        openable = [target_path]
    return Result(True, openable = openable)
