#!/usr/bin/env python3

import re
import argparse
import json
import sys
import errno
from contextlib import contextmanager
from datetime import datetime
from os import path, walk, makedirs, rmdir, scandir
from shutil import copy as shcopy, move as shmove
from subprocess import run

# local packages
import formatters.markdown

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

        self.data = self._merge_settings(loaded)

    def _merge_settings(self, new_data, dest = None):
        if not dest:
            dest = self.data

        for k, v in new_data.items():
            if isinstance(dest[k], dict):
                dest[k] = self._merge_settings(v, dest[k])
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

def main(argv):
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
    subparsers = parser.add_subparsers(title='Subcommands', description="Commands that can be run on the current campaign")

    # Subcommand to create the basic directories
    parser_init = subparsers.add_parser('init', help="Set up the basic directory structure for campaign files")
    parser_init.set_defaults(func=do_init)

    # Session subcommand
    parser_session = subparsers.add_parser('session', aliases=['s'], help="Create files for a new game session")
    parser_session.set_defaults(func=do_session)

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

    # Update files subcommand
    parser_update = subparsers.add_parser('update', parents=[paths_parser], help="Update various support files (motleys, etc.) using the content of the character files")
    parser_update.set_defaults(func=do_update)

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

    args = parser.parse_args(argv)

    result = args.func(args, prefs)

    if not result.success:
        print(result.errmsg)
        return result.errcode

    if result.openable and not args.batch:
        run([prefs.get("editor")] + result.openable)

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
    if args.court is not None:
        target_path = _add_path_if_exists(target_path, args.court.title())
    else:
        target_path = _add_path_if_exists(target_path, 'Courtless')

    for group_raw in args.group:
        group_name = group_raw.title()
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    # Create tags
    seeming_name = args.seeming.title()
    kith_name = args.kith.title()
    tags = ['@changeling %s %s' % (seeming_name, kith_name)]
    if args.motley is not None:
        tags.append('@motley %s' % args.motley)
    if args.court is not None:
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

    # Derive destination path
    target_path = _add_path_if_exists(prefs.get('paths.characters'), prefs.get('type_paths.%s' % ctype))
    for group_raw in args.group:
        group_name = group_raw.title()
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

def do_update(args, prefs):
    characters = []
    for search_path in args.search:
        characters.extend(_parse(search_path, args.ignore))
    # foreach motley tag in the characters
    #   ensure the corresponding motley file exists
    #   ensure the character appears in the list of motley members
    return Result(False, errmsg="Not yet implemented", errcode=3)

def do_reorg(args, prefs):
    characters = []
    for search_path in args.search:
        characters.extend(_parse(search_path, args.ignore))
    for c in characters:
        new_path = _create_path(c, base_path, prefs)
        if new_path != path.dirname(c['path']):
            if args.verbose:
                print("Moving {} to {}".format(c['path'], new_path))
            shmove(c['path'], new_path)

    if args.purge:
        for dirpath, dirnames, files in walk(base_path):
            try:
                rmdir(dirpath)
            except OSError as e:
                if e.errno == errno.ENOTEMPTY:
                    continue
            else:
                if args.verbose:
                    print("Removing empty directory {}".format(dirpath))

    return Result(True)

def _create_path(c, target_path, prefs):
    # add type-based directory if we can
    if 'type' in c:
        ctype = c['type'][0].lower()
        target_path = _add_path_if_exists(target_path, prefs.get('type_paths.%s' % ctype))
    else:
        ctype = 'none'

    # handle type-specific considerations
    if ctype == 'changeling':
        # changelings use court first, then groups
        if 'court' in c is not None:
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
    characters = []
    for search_path in args.search:
        characters.extend(_parse(search_path, args.ignore))
    characters = _sort_chars(characters)

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
    characters = []
    for search_path in args.search:
        characters.extend(_parse(search_path, args.ignore))

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
                # make sure our seeming and kith data is loaded
                if not sk:
                    try:
                        sk = _load_json(changeling_bonuses)
                    except IOError as e:
                        return Result(False, errmsg=e.strerror + " (%s)" % changeling_bonuses, errcode=4)

                # find (and fix) changeling-specific problems in the body of the sheet
                problems.extend(_lint_changeling(c, sk, args.fix))

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

def _lint_changeling(c, sk, fix = False):
    """Verify the more complex elements in a changeling sheet

    This method checks for changeling-specific problems within the rules blocks
    of the character sheet. The problems it checks for relate to the seeming and
    kith notes.

    1. Both elements must appear in the sheet's body -- not just the tags.
    2. Both elements must match the value of the corresponding tag.
    3. Both elements must have correct notes about its blessing (and curse for
        Seeming)

    Missing or incorrect notes can be fixed automatically if desired.
    """
    problems = []
    dirty = False

    seeming_regex = '^(?P<name>\s+seeming\s+)(?P<seeming>%s)\s*(?P<notes>\(.*\))?$'
    kith_regex = '^(?P<name>\s+kith\s+)(?P<kith>%s)\s*(?P<notes>\(.*\))?$'

    # Check that seeming tag exists and is valid
    seeming_tags = None
    if not 'seeming' in c:
        problems.append("Missing @seeming tag")
    else:
        seeming_tags = [t.lower() for t in c['seeming']] # used later
        for seeming_name in c['seeming']:
            if seeming_name.lower() not in sk['blessing']:
                problems.append("Unrecognized @seeming '%s'" % seeming_name)

    # Check that kith tag exists and is valid
    kith_tags = None
    if not 'kith' in c:
        problems.append("Missing @kith tag")
    else:
        kith_tags = [t.lower() for t in c['kith']] # used later
        for kith_name in c['kith']:
            if kith_name.lower() not in sk['blessing']:
                problems.append("Unrecognized @kith '%s'" % kith_name)

    # tags are ok. now compare against listed seeming and kith in stats

    with open(c['path'], 'r') as f:
        data = f.read()

        if seeming_tags:
            # ensure the listed seemings match our seeming tags
            seeming_re = re.compile(
                seeming_regex % '\w+',
                re.MULTILINE | re.IGNORECASE
            )
            seeming_matches = list(seeming_re.finditer(data))
            if set(seeming_tags) != set([m.group('seeming').lower() for m in seeming_matches]):
                problems.append("Seeming stats do not match @seeming tags")
            else:
                # tags and stats match. iterate through each seeming and make sure the notes are right
                for m in list(seeming_matches):
                    seeming_tag = m.group('seeming').lower()
                    if not seeming_tag in sk['blessing']:
                        continue

                    loaded_seeming_notes = m.group('notes')
                    seeming_notes = "(%s; %s)" % (sk['blessing'][seeming_tag], sk['curse'][seeming_tag])
                    if not loaded_seeming_notes:
                        problems.append("Missing notes for Seeming '%s'" % m.group('seeming'))
                        if fix:
                            data = _fix_seeming_notes(m.group('seeming'), seeming_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'
                    else:
                        if loaded_seeming_notes != seeming_notes:
                            problems.append("Incorrect notes for Seeming '%s'" % m.group('seeming'))
                            if fix:
                                data = _fix_seeming_notes(m.group('seeming'), seeming_notes, data)
                                problems[-1] += ' (FIXED)'
                                dirty = True
                            else:
                                problems[-1] += ' (can fix)'


        if kith_tags:
            # ensure the listed kiths match our kith tags
            kith_re = re.compile(
                kith_regex % '\w+',
                re.MULTILINE | re.IGNORECASE
            )
            kith_matches = list(kith_re.finditer(data))
            if set(kith_tags) != set([m.group('kith').lower() for m in kith_matches]):
                problems.append("Kith stats do not match @kith tags")
            else:
                # tags and stats match. iterate through each kith and make sure the notes are right
                for m in list(kith_matches):
                    kith_tag = m.group('kith').lower()
                    if not kith_tag in sk['blessing']:
                        continue

                    loaded_kith_notes = m.group('notes')
                    kith_notes = "(%s)" % (sk['blessing'][kith_tag])
                    if not loaded_kith_notes:
                        problems.append("Missing notes for Kith '%s'" % m.group('kith'))
                        if fix:
                            data = _fix_kith_notes(m.group('kith'), kith_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'
                    else:
                        if loaded_kith_notes != kith_notes:
                            problems.append("Incorrect notes for Kith '%s'" % m.group('kith'))
                            if fix:
                                data = _fix_kith_notes(m.group('kith'), kith_notes, data)
                                problems[-1] += ' (FIXED)'
                                dirty = True
                            else:
                                problems[-1] += ' (can fix)'

    if dirty and data:
        with open(c['path'], 'w') as f:
            f.write(data)

    return problems

def _fix_seeming_notes(seeming, notes, data):
    """Insert correct notes for a seeming stat"""
    seeming_regex = '^(?P<name>\s+seeming\s+)(?P<seeming>%s)\s*(?P<notes>\(.*\))?$'
    seeming_fix_re = re.compile(
        seeming_regex % seeming,
        re.MULTILINE | re.IGNORECASE
    )
    return seeming_fix_re.sub(
        '\g<1>\g<2> %s' % notes,
        data
    )

def _fix_kith_notes(kith, notes, data):
    """Insert correct notes for a kith stat"""
    kith_regex = '^(?P<name>\s+kith\s+)(?P<kith>%s)\s*(?P<notes>\(.*\))?$'
    kith_fix_re = re.compile(
        kith_regex % kith,
        re.MULTILINE | re.IGNORECASE
    )
    return kith_fix_re.sub(
        '\g<1>\g<2> %s' % notes,
        data
    )

def do_init(args, prefs):
    """Create the basic directories for a campaign

    This will create the directories this tool expects to find within a
    campaign. Other directories are left to the user.
    """
    for k, p in prefs.get('paths').items():
        makedirs(p, mode=0o775, exist_ok=True)

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

def _parse(search_root, ignore_paths = [], include_bare = False):
    """Parse all the character files in a directory

    Set include_bare to True to scan files without an extension in addition to
    .nwod files.
    """
    if path.isfile(search_root):
        data = _parse_character(search_root)
        data['path'] = search_root
        return [data]

    characters = []
    for dirpath, dirnames, files in walk(search_root, followlinks=True):
        if dirpath in ignore_paths:
            continue
        for name in files:
            target_path = path.join(dirpath, name)
            if target_path in ignore_paths:
                continue
            base, ext = path.splitext(name)
            if ext == '.nwod' or (include_bare and not ext):
                data = _parse_character(target_path)
                data['path'] = target_path
                characters.append(data)

    return characters

def _parse_character(char_file_path):
    """Parse a single character file"""
    name_re = re.compile('([\w\s]+)(?: - )?.*')
    section_re = re.compile('^--.+--\s*$')
    tag_re = re.compile('^@(?P<tag>\w+)\s+(?P<value>.*)$')

    # Group-like tags. These all accept an accompanying `rank` tag.
    group_tags = ['group', 'court', 'motley']

    # derive character name from basename
    basename = path.basename(char_file_path)
    match = name_re.match(path.splitext(basename)[0])
    name = match.group(1)

    # rank uses a dict keyed by group name instead of an array
    # description is always a plain string
    char_properties = {'name': [name], 'description': '', 'rank': {}}

    with open(char_file_path, 'r') as char_file:
        last_group = ''
        previous_line_empty = False

        for line in char_file:
            if section_re.match(line):
                break

            match = tag_re.match(line)
            if match is not None:
                tag = match.group('tag')
                value = match.group('value')

                if tag == 'changeling':
                    bits = value.split()
                    char_properties.setdefault('type', []).append('Changeling')
                    if len(bits):
                        char_properties.setdefault('seeming', []).append(bits[0])
                    if len(bits) > 1:
                        char_properties.setdefault('kith', []).append(bits[1])
                    continue

                if tag == 'realname':
                    char_properties['name'][0] = value
                    continue

                if tag in group_tags:
                    last_group = value

                if tag == 'rank' and last_group:
                    char_properties['rank'].setdefault(last_group, []).append(value)
                    continue
            else:
                if line == "\n":
                    if not previous_line_empty:
                        previous_line_empty = True
                    else:
                        continue
                else:
                    previous_line_empty = False

                char_properties['description'] += line
                continue

            char_properties.setdefault(tag, []).append(value)

    char_properties['description'] = char_properties['description'].strip()
    return char_properties

if __name__ == '__main__':
    main(sys.argv[1:])
