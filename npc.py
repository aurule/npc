#!/usr/bin/env python3

import re
from os import path, listdir, walk
import argparse
import shutil import copy as shcopy
import json
from subprocess import call

# TODO cli args
# scanning:
#   search_root
#   paths to ignore

# Regexes for parsing important elements
plot_regex = '^plot (\d+)$'
session_regex = '^session (\d+)$'

class Result:
    """Holds data about the result of a subcommand"""
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
    """Stores settings for later use"""
    install_base = path.dirname(path.realpath(__file__))
    path_default = path.join(install_base, 'support/settings-default.json')

    def __init__(self, settings_path = path_default):
        self.settings_files = [_load_json(settings_path)]
        self._localize_default_paths()

    def get(self, key):
        """Get the value of a settings key"""
        key_parts = key.split('.')
        arr = self.settings_files[0]
        for k in key_parts:
            try:
                arr = arr[k]
            except KeyError:
                return None
        return arr

    def _localize_default_paths(self):
        """Make a set of paths local to the script installation directory"""
        paths = self.settings_files[0]['templates']
        for k, v in paths.items():
            paths[k] = path.join(self.install_base, v)

def main():
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

    parser_session = subparsers.add_parser('session', aliases=['s'], help="Create files for a new game session")
    parser_session.set_defaults(func=create_session)

    parser_update = subparsers.add_parser('update', aliases=['u'], help="Update various support files (motleys, etc.) using the content of the character files")
    parser_update.set_defaults(funct=update_dependencies)

    parser_webpage = subparsers.add_parser('webpage', aliases=['web', 'w'], help="Generate an NPC Listing")
    parser_webpage.set_defaults(funct=make_webpage)

    parser_lint = subparsers.add_parser('lint', help="Check the character files for minimum completeness.")
    parser_lint.add_argument('-f', '--fix', action='store_true', default=False, help="Automatically fix some problems")
    parser_lint.set_defaults(func=lint)

    args = parser.parse_args()

    prefs = Settings()

    result = args.func(args, prefs)

    if not result.success:
        print(result.errmsg)
        return result.errcode

    if result.openable and not args.batch:
        call([prefs.get("editor")] + result.openable)

def create_changeling(args, prefs):
    changeling_bonuses = path.join(prefs.install_base, 'support/seeming-kith.json')
    seeming_re = re.compile(
        '^(\s+)seeming(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        '^(\s+)kith(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )

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

    seeming_name = args.seeming.title()
    kith_name = args.kith.title()
    tags = ['@changeling %s %s' % (seeming_name, kith_name)]
    if args.motley is not None:
        tags.append('@motley %s' % args.motley)
    if args.court is not None:
        tags.append('@court %s' % args.court.title())
    tags.extend(["@group %s" % g for g in args.group])

    header = "\n".join(tags) + '\n\n'

    try:
        with open(prefs.get('templates.changeling'), 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % prefs.get('templates.changeling'), errcode=4)

    # insert seeming and kith in advantages block
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

    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def create_human(args, prefs):
    target_path = _add_path_if_exists(prefs.get('paths.characters'), 'Humans')
    for group_raw in args.group:
        group_name = group_raw.title()
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    tags = ['@type Human'] + ["@group %s" % g for g in args.group]
    header = "\n".join(tags) + '\n\n'

    try:
        with open(prefs.get('templates.human'), 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % prefs.get('templates.human'), errcode=4)

    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def _add_path_if_exists(base, potential):
    test_path = path.join(base, potential)
    if path.exists(test_path):
        return test_path
    return base

def create_session(args, prefs):
    session_template = path.expanduser("~/Templates/Session Log.md")

    plot_files = [f for f in listdir(prefs.get('paths.plot')) if _is_plot_file(f, prefs)]
    latest_plot = max(plot_files, key=lambda plot_files:re.split(r"\s", plot_files)[1])
    (latest_plot_name, latest_plot_ext) = path.splitext(latest_plot)
    plot_match = re.match(plot_regex, latest_plot_name)
    plot_number = int(plot_match.group(1))

    session_files = [f for f in listdir(prefs.get('paths.session')) if _is_session_file(f, prefs)]
    latest_session = max(session_files, key=lambda session_files:re.split(r"\s", session_files)[1])
    (latest_session_name, latest_session_ext) = path.splitext(latest_session)
    session_match = re.match(session_regex, latest_session_name)
    session_number = int(session_match.group(1))

    if plot_number != session_number:
        return Result(False, errmsg="Cannot create new plot and session files: latest files have different numbers (plot %i, session %i)" % (plot_number, session_number), errcode=2)

    new_number = plot_number + 1

    old_plot_path = path.join(prefs.get('paths.plot'), latest_plot)
    new_plot_path = path.join(prefs.get('paths.plot'), ("plot %i" % new_number) + latest_plot_ext)
    shcopy(old_plot_path, new_plot_path)

    old_session_path = path.join(prefs.get('paths.session'), latest_session)
    new_session_path = path.join(prefs.get('paths.session'), ("session %i" % new_number) + latest_session_ext)
    shcopy(session_template, new_session_path)

    return Result(True, openable=[new_session_path, new_plot_path, old_plot_path, old_session_path])

def _is_plot_file(f, prefs):
    really_a_file = path.isfile(path.join(prefs.get('paths.plot'), f))
    basename = path.basename(f)
    match = re.match(plot_regex, path.splitext(basename)[0])

    return really_a_file and match

def _is_session_file(f, prefs):
    really_a_file = path.isfile(path.join(prefs.get('paths.session'), f))
    basename = path.basename(f)
    match = re.match(session_regex, path.splitext(basename)[0])

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
    characters = _parse(prefs.get('paths.characters'))
    for c in characters:
        # ensure each character at least has a description and @type tag
        # ensure every changeling sheet has correct notes for seeming and kith
        # show a warning for each infraction
        # fix automatically if possible and args.fix
        pass

    return Result(False, errmsg="Not yet implemented", errcode=3)

if __name__ == '__main__':
    main()

def _parse(search_root, ignore_paths = []):
    characters = []
    for dirpath, dirnames, files in walk(search_root):
        if dirpath in ignore_paths:
            continue
        for name in files:
            base, ext = path.splitext(name)
            if ext in valid_exts or not ext:
                characters.append(parse_character(path.join(dirpath, name)))

    return characters

def _parse_character(char_file_path):
    name_re = re.compile('([\w\s]+)(?: - )?.*')
    section_re = re.compile('^--.+--\s*$')
    tag_re = re.compile('^@(?P<tag>\w+)\s+(?P<value>.*)$')

    # Group-like tags. These all accept an accompanying `rank` tag.
    group_tags = ['group', 'court', 'motley']

    # Recognized extensions
    valid_exts = ('.nwod')

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
