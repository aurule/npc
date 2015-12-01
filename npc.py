#!/usr/bin/env python3

import re
import os
import argparse

# TODO cli args
# scanning:
#   search_root
#   paths to ignore

def main():
    parser = argparse.ArgumentParser(description = 'GM helper script to manage game files')
    parser.add_argument('-o', '--open', action='store_true', default=False, help="immediately open all newly created files")
    subparsers = parser.add_subparsers()

    parser_changeling = subparsers.add_parser('changeling')
    parser_changeling.set_defaults(func=create_changeling)
    parser_changeling.add_argument('name', help="character's name", metavar='name')
    parser_changeling.add_argument('seeming', help="character's Seeming", metavar='seeming')
    parser_changeling.add_argument('kith', help="character's Kith", metavar='kith')
    parser_changeling.add_argument('-c', '--court', help="the character's Court", metavar='court')
    parser_changeling.add_argument('-m', '--motley', help="the character's Motley", metavar='motley')
    parser_changeling.add_argument('-g', '--group', help='name of a group that counts the character as a member', metavar='group')

    parser_human = subparsers.add_parser('human')
    parser_human.set_defaults(func=create_human)
    parser_human.add_argument('name', help="character's name", metavar='name')
    parser_human.add_argument('-g', '--group', help='name of a group that counts the character as a member', metavar='group')

    parser_update = subparsers.add_parser('update', aliases=['u'])
    parser_update.set_defaults(funct=update_dependencies)

    parser_webpage = subparsers.add_parser('webpage', aliases=['web', 'w'])
    parser_webpage.set_defaults(funct=make_webpage)

    args = parser.parse_args()
    args.func(args)

def create_changeling(args):
    characters_root = 'Characters'

    # derive folder location
    #   if a folder exists named Changelings, add to path
    #   if a folder exists named args.court, add to path
    #   foreach args.group in order, if a folder exists, add to path
    # ensure the character does not already exist
    # store monolithic string from changeling template
    # prepend tags as appropriate
    #   @changeling args.seeming args.kith
    #   @court
    #   @motley
    #   @group
    # insert seeming and kith in advantages block
    #   look up curse and blessings
    # write to new file

def create_changeling(args):
    characters_root = 'Characters'

    # derive folder location
    #   if a folder exists named Humans, add to path
    #   foreach args.group in order, if a folder exists, add to path
    # ensure the character does not already exist
    # store monolithic string from human template file
    # prepend tags as appropriate
    #   @type Human
    #   @group
    # write to new file

def update_dependencies(args):
    # parse characters
    # foreach motley tag in the characters
    #   ensure the corresponding motley file exists
    #   ensure the character appears in the list of motley members
    pass

def make_webpage(args):
    # parse characters
    # sort them?
    # add html snippets for each character
    # output a final html file
    pass

if __name__ == '__main__':
    main()

# Regexes for parsing important elements
name_regex = '([\w\s]+)(?: - )?.*'
section_regex = '^--.+--\s*$'
tag_regex = '^@(?P<tag>\w+)\s+(?P<value>.*)$'

# Group-like tags. These all accept an accompanying `rank` tag.
group_tags = ['group', 'court', 'motley']

# Recognized extensions
valid_exts = ('.nwod')

def parse(search_root, ignore_paths = []):
    search_root = '.'

    characters = []
    for dirpath, dirnames, files in os.walk(search_root):
        if dirpath in ignore_paths:
            continue
        for name in files:
            base, ext = os.path.splitext(name)
            if ext in valid_exts or not ext:
                characters.append(parse_character(os.path.join(dirpath, name)))

    return characters

def parse_character(char_file_path):
    name_re = re.compile(name_regex)
    section_re = re.compile(section_regex)
    tag_re = re.compile(tag_regex)

    # derive character name from basename
    basename = os.path.basename(char_file_path)
    match = name_re.match(os.path.splitext(basename)[0])
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
