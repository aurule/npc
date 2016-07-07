#!/usr/bin/env python3.5

import re
import itertools
from os import path, walk
from collections import defaultdict

def get_characters(search_paths = ['.'], ignore_paths = []):
    """
    Get data from character files

    Args:
        search_paths (list): Paths to search for character files
        ignore_paths (list): Paths to exclude from the search

    Returns:
        List of dictionaries containing parsed character information
    """
    return itertools.chain.from_iterable((_parse_path(path, ignore_paths) for path in search_paths))

def _parse_path(start_path, ignore_paths = [], include_bare = False):
    """
    Parse all the character files under a directory

    Args:
        start_path (str): Path to search
        ignore_paths (list): Pathsh to exclude
        include_bare (bool): Whether to attempt to parse files without an
            extension in addition to .nwod files.

    Returns:
        List of dictionaries containing parsed character data
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
    """
    Recursively traverse a directory tree while ignoring certain paths.

    Args:
        root (str): Directory to start at
        ignore (list): Paths to skip over

    Yields:
        A tuple (path, [dirs], [files]) as from `os.walk`.
    """
    def included(d):
        """
        Determine whether a path should be searched

        Only skips this path if it, or its parent, is explicitly in the `ignore`
        list.

        Args:
            d (str): The path to check

        Returns:
            True if d should be searched, false if it should be ignored
        """
        return (path.join(dirpath, d) not in ignore) and (dirpath not in ignore)

    for dirpath, dirnames, filenames in walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if included(d)]
        yield dirpath, dirnames, filenames

def _parse_character(char_file_path):
    """
    Parse a single character file

    Args:
        char_file_path (str): Path to the character file to parse

    Returns:
        Dictionary of character data. Most keys store a list of values from the
        character. The `description` key stores a simple string, and the `rank`
        key stores a dict of list entries. Those keys are individual group
        names.
    """
    name_re = re.compile('(?P<name>\w+(\s\w+)*)(?: - )?.*')
    section_re = re.compile('^--.+--\s*$')
    tag_re = re.compile('^@(?P<tag>\w+)\s+(?P<value>.*)$')

    # Group-like tags. These all accept an accompanying `rank` tag.
    group_tags = ['group', 'court', 'motley']

    # derive character name from basename
    basename = path.basename(char_file_path)
    match = name_re.match(path.splitext(basename)[0])
    name = match.group('name')

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
                if tag == 'rank':
                    if last_group:
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
