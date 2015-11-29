#!/usr/bin/python3

import re
import os
import argparse

# TODO cli args
# search_root
# paths to ignore

def main():
    parser = argparse.ArgumentParser(description = 'GM helper script to manage game files')
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser('new')
    parser_new.set_defaults(func=create_new)
    # parser_new.add_argument('artifact', choices=[''], required=True, help='The type of object to create', metavar='object', dest='typename')

    args = parser.parse_args()
    args.func(args)

def create_new(args):
    # create a new object
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
