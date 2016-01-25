#!/usr/bin/env python3.5

import re
import itertools
from os import path, walk
from collections import defaultdict

def get_characters(search_paths = ['.'], ignore_paths = []):
    return itertools.chain.from_iterable((_parse_path(path, ignore_paths) for path in search_paths))

def _parse_path(start_path, ignore_paths = [], include_bare = False):
    """Parse all the character files in a directory

    Set include_bare to True to scan files without an extension in addition to
    .nwod files.
    """
    if path.isfile(start_path):
        return [_parse_character(start_path)]

    characters = []
    for dirpath, _, files in _walk_ignore(start_path, ignore_paths):
        for name in files:
            target_path = path.join(dirpath, name)
            if target_path in ignore_paths:
                continue
            base, ext = path.splitext(name)
            if ext == '.nwod' or (include_bare and not ext):
                data = _parse_character(target_path)
                characters.append(data)
    return characters

def _walk_ignore(root, ignore):
    def included(d):
        return (path.join(dirpath, d) not in ignore) and (dirpath not in ignore)

    for dirpath, dirnames, filenames in walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if included(d)]
        yield dirpath, dirnames, filenames

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
    char_properties = defaultdict(list)
    char_properties.update({'name': [name], 'description': '', 'rank': defaultdict(list)})

    with open(char_file_path, 'r') as char_file:
        last_group = ''
        previous_line_empty = False

        for line in char_file:
            # stop processing once we see game stats
            if section_re.match(line):
                break

            match = tag_re.match(line)
            if match:
                tag = match.group('tag')
                value = match.group('value')

                if tag == 'changeling':
                    bits = value.split(maxsplit=1)
                    char_properties['type'].append('Changeling')
                    if len(bits):
                        char_properties['seeming'].append(bits[0])
                    if len(bits) > 1:
                        char_properties['kith'].append(bits[1])
                    continue

                if tag == 'realname':
                    char_properties['name'][0] = value
                    continue

                if tag in group_tags:
                    last_group = value
                if tag == 'rank' and last_group:
                    char_properties['rank'][last_group].append(value)
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

            char_properties[tag].append(value)

    char_properties['description'] = char_properties['description'].strip()
    char_properties['path'] = char_file_path
    return char_properties
