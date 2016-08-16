"""
Parse character files into Character objects

The main entry point is get_characters, which creates a list of characters. To
parse a single file, use parse_character instead.
"""

import re
import itertools
from os import path, walk
from .util import Character

VALID_EXTENSIONS = ['.nwod']
"""tuple: file extensions that should be parsed"""

def get_characters(search_paths=None, ignore_paths=None):
    """
    Get data from character files

    Normalizes the ignore paths with os.path.normpath.

    Args:
        search_paths (list): Paths to search for character files
        ignore_paths (list): Paths to exclude from the search

    Returns:
        List of Characters generated from every parseable character file within
        every path of search_paths, but not in ignore_paths.
    """
    if search_paths is None:
        search_paths = ['.']

    if ignore_paths:
        ignore_paths[:] = [path.normpath(d) for d in ignore_paths]

    return itertools.chain.from_iterable((_parse_path(path, ignore_paths) for path in search_paths))

def _parse_path(start_path, ignore_paths=None, include_bare=False):
    """
    Parse all the character files under a directory

    Args:
        start_path (str): Path to search
        ignore_paths (list): Paths to exclude. Assumed to be normalized, as from
            os.path.normpath.
        include_bare (bool): Whether to attempt to parse files without an
            extension in addition to .nwod files.

    Returns:
        List of Characters generated from every parseable character file within
        start_path, but not in ignore_paths.
    """
    if path.isfile(start_path):
        return [parse_character(start_path)]
    if ignore_paths is None:
        ignore_paths = []

    characters = []
    for dirpath, _, files in _walk_ignore(start_path, ignore_paths):
        for name in files:
            target_path = path.join(dirpath, name)
            if target_path in ignore_paths:
                # skip ignored files
                continue
            _, ext = path.splitext(name)
            if ext in VALID_EXTENSIONS or (include_bare and not ext):
                data = parse_character(target_path)
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
    def should_search(base, check):
        """
        Determine whether a path should be searched

        Only skips this path if it, or its parent, is explicitly in the `ignore`
        list.

        Args:
            base (str): Parent path
            check (str): The path to check

        Returns:
            True if d should be searched, false if it should be ignored
        """
        return base not in ignore \
            and path.join(base, check) not in ignore

    for dirpath, dirnames, filenames in walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if should_search(dirpath, d)]
        yield dirpath, dirnames, filenames

def parse_character(char_file_path: str) -> Character:
    """
    Parse a single character file

    Args:
        char_file_path (str): Path to the character file to parse

    Returns:
        Character object. Most keys store a list of values from the character.
        The `description` key stores a simple string, and the `rank` key stores
        a dict of list entries. Those keys are individual group names.
    """
    name_re = re.compile(r'(?P<name>[\w]+\.?(?:\s[\w.]+)*)(?: - )?.*')
    section_re = re.compile(r'^--.+--\s*$')
    tag_re = re.compile(r'^@(?P<tag>\w+)\s+(?P<value>.*)$')

    # Group-like tags. These all accept an accompanying `rank` tag.
    group_tags = ['group', 'court', 'motley']

    # derive character name from basename
    basename = path.basename(char_file_path)
    match = name_re.match(path.splitext(basename)[0])

    # instantiate new character
    parsed_char = Character(
        name=[match.group('name')],
        path=char_file_path
    )

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
                    # grab attributes from compound tag
                    bits = value.split(maxsplit=1)
                    parsed_char.append('type', 'Changeling')
                    if len(bits):
                        parsed_char.append('seeming', bits[0])
                    if len(bits) > 1:
                        parsed_char.append('kith', bits[1])
                    continue

                if tag == 'realname':
                    # replace the first name
                    parsed_char['name'][0] = value
                    continue

                if tag in group_tags:
                    last_group = value
                if tag == 'rank':
                    if last_group:
                        parsed_char.append_rank(last_group, value)
                    continue
            else:
                if line == "\n":
                    if not previous_line_empty:
                        previous_line_empty = True
                    else:
                        continue
                else:
                    previous_line_empty = False

                parsed_char.append('description', line)
                continue

            parsed_char.append(tag, value)

    parsed_char['description'] = parsed_char['description'].strip()
    return parsed_char
