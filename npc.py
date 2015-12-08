#!/usr/bin/env python3

import re
import argparse
import json
from os import path, listdir, walk, makedirs
from shutil import copy as shcopy
from subprocess import call

# Regexes for parsing important elements
plot_re = re.compile('^plot (\d+)$')
session_regex = '^session (\d+)$'

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

    def __init__(self, settings_path = path_default):
        self.settings_files = [_load_json(settings_path)]
        self._localize_default_paths()

    def get(self, key):
        """Get the value of a settings key

        Use the period character to indicate a nested key.
        """
        key_parts = key.split('.')
        arr = self.settings_files[0]
        for k in key_parts:
            try:
                arr = arr[k]
            except KeyError:
                return None
        return arr

    def _localize_default_paths(self):
        """Expand some default paths so they point to script install directory"""
        paths = self.settings_files[0]['templates']
        for k, v in paths.items():
            paths[k] = path.join(self.install_base, v)

def main():
    """Run the interface"""

    parser = argparse.ArgumentParser(description = 'GM helper script to manage game files')
    parser.add_argument('-b', '--batch', action='store_true', default=False, help="Do not open any newly created files")
    subparsers = parser.add_subparsers(title='Subcommands', description="Commands that can be run on the current campaign", metavar="changeling, human, session, update, webpage, lint")

    parser_changeling = subparsers.add_parser('changeling', aliases=['c'], help="Create a new changeling character")
    parser_changeling.set_defaults(func=create_changeling)
    parser_changeling.add_argument('name', help="character's name", metavar='name')
    parser_changeling.add_argument('seeming', help="character's Seeming", metavar='seeming')
    parser_changeling.add_argument('kith', help="character's Kith", metavar='kith')
    parser_changeling.add_argument('-c', '--court', help="the character's Court", metavar='court')
    parser_changeling.add_argument('-m', '--motley', help="the character's Motley", metavar='motley')
    parser_changeling.add_argument('-g', '--group', default=[], nargs="*", help='name of a group that counts the character as a member', metavar='group')

    parser_human = subparsers.add_parser('human', aliases=['h'], help="Create a new human character")
    parser_human.set_defaults(func=create_human)
    parser_human.add_argument('name', help="character's name", metavar='name')
    parser_human.add_argument('-g', '--group', default=[], nargs="*", help='name of a group that counts the character as a member', metavar='group')

    parser_fetch = subparsers.add_parser('fetch', aliases=['f'], help="Create a new fetch character")
    parser_fetch.set_defaults(func=create_fetch)
    parser_fetch.add_argument('name', help="character's name", metavar='name')
    parser_fetch.add_argument('-g', '--group', default=[], nargs="*", help='name of a group that counts the character as a member', metavar='group')

    parser_goblin = subparsers.add_parser('goblin', help="Create a new goblin character")
    parser_goblin.set_defaults(func=create_goblin)
    parser_goblin.add_argument('name', help="character's name", metavar='name')
    parser_goblin.add_argument('-g', '--group', default=[], nargs="*", help='name of a group that counts the character as a member', metavar='group')

    parser_session = subparsers.add_parser('session', aliases=['s'], help="Create files for a new game session")
    parser_session.set_defaults(func=create_session)

    parser_update = subparsers.add_parser('update', aliases=['u'], help="Update various support files (motleys, etc.) using the content of the character files")
    parser_update.set_defaults(funct=update_dependencies)

    parser_webpage = subparsers.add_parser('list', aliases=['l'], help="Generate an NPC Listing")
    parser_webpage.add_argument('-o', '--outfile', nargs="?", help="file where the listing will be saved")
    parser_webpage.set_defaults(funct=make_webpage)

    parser_lint = subparsers.add_parser('lint', help="Check the character files for minimum completeness.")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="automatically fix certain problems")
    parser_lint.set_defaults(func=lint)
    # TODO add more args
    #   search_root
    #   paths to ignore
    #   list of explicit paths to lint

    parser_init = subparsers.add_parser('init', help="Set up the basic directory structure for campaign files")
    parser_init.set_defaults(func=init_dirs)

    args = parser.parse_args()
    prefs = Settings()

    result = args.func(args, prefs)

    if not result.success:
        print(result.errmsg)
        return result.errcode

    if result.openable and not args.batch:
        call([prefs.get("editor")] + result.openable)

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
    changeling_bonuses = path.join(prefs.install_base, 'support/seeming-kith.json')
    seeming_re = re.compile(
        '^(\s+)seeming(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        '^(\s+)kith(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )

    # Derive the path for the new file
    target_path = _add_path_if_exists(prefs.get('paths.characters'), 'Changelings')
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
    seeming_notes = "%s; %s" % (sk['blessing'][args.seeming.lower()], sk['curse'][args.seeming.lower()])
    kith_notes = sk['blessing'][args.kith.lower()]
    data = seeming_re.sub(
        '\g<1>Seeming\g<2>%s (%s)' % (seeming_name, seeming_notes),
        data
    )
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

def create_human(args, prefs):
    """Create a new Human character"""
    target_path = _add_path_if_exists(prefs.get('paths.characters'), 'Humans')
    template = prefs.get('templates.human')
    return _create_simple_character(args, target_path, template, 'Human')

def create_fetch(args, prefs):
    """Create a new Fetch character"""
    target_path = _add_path_if_exists(prefs.get('paths.characters'), 'Fetches')
    template = prefs.get('templates.fetch')
    return _create_simple_character(args, target_path, template, 'Fetch')

def create_goblin(args, prefs):
    """Create a new Goblin character"""
    target_path = _add_path_if_exists(prefs.get('paths.characters'), 'Goblins')
    template = prefs.get('templates.goblin')
    return _create_simple_character(args, target_path, template, 'Goblin')

def _create_simple_character(args, target_path, template, typetag):
    """Create a character without extra processing

    Simple characters don't have any unique tags or file annotations. This
    method is used by create_human() and create_fetch().

    Arguments:
    * args          object  Object with runtime data. Must contain the following
                            attributes:
        + name              string  Base file name
        + group (optional)  list    One or more names of groups the character
                                    belongs to. Used to derive path for the file.
    * target_path   string  Base destination of the created file. This is
                            modified to get the final destination folder.
    * template      string  Path to the template file to copy
    * typetag       string  Name of the character's type. Inserted as @type tag.
    """
    # Derive destination path
    for group_raw in args.group:
        group_name = group_raw.title()
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    # Add tags
    tags = ['@type %s' % typetag] + ["@group %s" % g for g in args.group]
    header = "\n".join(tags) + '\n\n'

    # Copy template
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

def create_session(args, prefs):
    """Creates the files for a new game session

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log.
    """
    session_template = path.expanduser("~/Templates/Session Log.md")

    # find latest plot file and its number
    plot_files = [f for f in listdir(prefs.get('paths.plot')) if _is_plot_file(f, prefs)]
    latest_plot = max(plot_files, key=lambda plot_files:re.split(r"\s", plot_files)[1])
    (latest_plot_name, latest_plot_ext) = path.splitext(latest_plot)
    plot_match = plot_re.match(latest_plot_name)
    plot_number = int(plot_match.group(1))

    # find latest session log and its number
    session_files = [f for f in listdir(prefs.get('paths.session')) if _is_session_file(f, prefs)]
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
    shcopy(session_template, new_session_path)

    return Result(True, openable=[new_session_path, new_plot_path, old_plot_path, old_session_path])

def _is_plot_file(f, prefs):
    """Get whether f is a plot file"""
    really_a_file = path.isfile(path.join(prefs.get('paths.plot'), f))
    basename = path.basename(f)
    match = plot_re.match(path.splitext(basename)[0])

    return really_a_file and match

def _is_session_file(f, prefs):
    """Get whether f is a session log"""
    really_a_file = path.isfile(path.join(prefs.get('paths.session'), f))
    basename = path.basename(f)
    match = session_re.match(path.splitext(basename)[0])

    return really_a_file and match

def update_dependencies(args, prefs):
    characters = _parse(prefs.get('paths.characters'))
    # foreach motley tag in the characters
    #   ensure the corresponding motley file exists
    #   ensure the character appears in the list of motley members
    return Result(False, errmsg="Not yet implemented", errcode=3)

def make_webpage(args, prefs):
    characters = _parse(prefs.get('paths.characters'))
    # sort them?
    # add html snippets for each character
    # output a final html file
    return Result(False, errmsg="Not yet implemented", errcode=3)

def lint(args, prefs):
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
    characters = _parse(prefs.get('paths.characters'))

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
            # Do special processing based on reported type
            if 'changeling' in c['type'][0].lower():
                if not sk:
                    try:
                        sk = _load_json(changeling_bonuses)
                    except IOError as e:
                        return Result(False, errmsg=e.strerror + " (%s)" % changeling_bonuses, errcode=4)

                # Check that seeming tag exists and is valid
                if not 'seeming' in c:
                    problems.append("Missing @seeming tag")
                else:
                    seeming_tag = c['seeming'][0].lower()
                    if seeming_tag not in sk['blessing']:
                        problems.append("Unrecognized @seeming '%s'" % seeming_tag.title())

                # Check that kith tag exists and is valid
                if not 'kith' in c:
                    problems.append("Missing @kith tag")
                else:
                    kith_tag = c['kith'][0].lower()
                    if kith_tag not in sk['blessing']:
                        problems.append("Unrecognized @kith '%s'" % kith_tag.title())

                # find (and fix) changeling-specific problems in the body of the sheet
                problems.extend(_fix_changeling(c, sk, args.fix))

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

def _fix_changeling(c, sk, fix = False):
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
    seeming_re = re.compile(
        '^(?P<name>\s+seeming\s+)(?P<seeming>\w+)\s*(?P<notes>\(.*\))?$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        '^(?P<name>\s+kith\s+)(?P<kith>\w+)\s*(?P<notes>\(.*\))?$',
        re.MULTILINE | re.IGNORECASE
    )
    with open(c['path'], 'r') as f:
        data = f.read()

        # Must list seeming
        seeming_match = seeming_re.search(data)
        if not seeming_match:
            problems.append("Missing Seeming in stats")
            # TODO might be able to create the annotation
        else:
            if 'seeming' in c:
                # Listed seeming must match @seeming tag
                seeming_tag = c['seeming'][0].lower()
                seeming_stat = seeming_match.group('seeming').lower()
                if seeming_stat != seeming_tag:
                    problems.append("Seeming stat '%s' does not match @seeming tag '%s'" % (seeming_stat.title(), seeming_tag.title()))
                else:
                    # Tag and annotation match. Now make sure the notes are present and correct.
                    loaded_seeming_notes = seeming_match.group('notes')
                    if not loaded_seeming_notes:
                        problems.append("Missing Seeming notes")
                        if fix:
                            seeming_notes = "(%s; %s)" % (sk['blessing'][seeming_tag], sk['curse'][seeming_tag])
                            data = seeming_re.sub(
                                '\g<1>\g<2> %s' % seeming_notes,
                                data
                            )
                            problems[-1] += ' (FIXED)'
                            dirty = True
                    else:
                        seeming_notes = "(%s; %s)" % (sk['blessing'][seeming_tag], sk['curse'][seeming_tag])
                        if loaded_seeming_notes != seeming_notes:
                            problems.append("Incorrect Seeming notes")
                            if fix:
                                data = seeming_re.sub(
                                    '\g<1>\g<2> %s' % seeming_notes,
                                    data
                                )
                                problems[-1] += ' (FIXED)'
                                dirty = True

        # Must list kith
        kith_match = kith_re.search(data)
        if not kith_match:
            problems.append("Missing Kith in stats")
            # TODO might be able to create the annotation
        else:
            if 'kith' in c:
                # Listed kith must match @kith tag
                kith_tag = c['kith'][0].lower()
                kith_stat = kith_match.group('kith').lower()
                if kith_stat != kith_tag:
                    problems.append("Kith stat '%s' does not match @kith tag '%s'" % (kith_stat.title(), kith_tag.title()))
                else:
                    # Tag and annotation match. Now make sure the notes are present and correct.
                    loaded_kith_notes = kith_match.group('notes')
                    if not loaded_kith_notes:
                        problems.append("Missing Kith notes")
                        if fix:
                            kith_notes = "(%s)" % sk['blessing'][c['kith'][0].lower()]
                            data = kith_re.sub(
                                '\g<1>\g<2> %s' % kith_notes,
                                data
                            )
                            problems[-1] += ' (FIXED)'
                            dirty = True
                    else:
                        kith_notes = "(%s)" % sk['blessing'][c['kith'][0].lower()]
                        if loaded_kith_notes != kith_notes:
                            problems.append("Incorrect Kith notes")
                            if fix:
                                data = kith_re.sub(
                                    '\g<1>\g<2> %s' % kith_notes,
                                    data
                                )
                                problems[-1] += ' (FIXED)'
                                dirty = True
    if dirty and data:
        with open(c['path'], 'w') as f:
            f.write(data)

    return problems

def init_dirs(args, prefs):
    """Create the basic directories for a campaign

    This will create the directories this tool expects to find within a
    campaign. Other directories are left to the user.
    """
    for k, p in prefs.get('paths').items():
        if not path.exists(p):
            makedirs(p)

    return Result(True)

def _parse(search_root, ignore_paths = [], include_bare = False):
    """Parse all the character files in a directory

    Set include_bare to True to scan files without an extension in addition to
    .nwod files.
    """
    characters = []
    for dirpath, dirnames, files in walk(search_root):
        if dirpath in ignore_paths:
            continue
        for name in files:
            base, ext = path.splitext(name)
            if ext == '.nwod' or (include_bare and not ext):
                target_path = path.join(dirpath, name)
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

    return char_properties

if __name__ == '__main__':
    main()
