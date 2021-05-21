"""
Parse character files into Character objects

The main entry point is get_characters, which creates a list of characters. To
parse a single file, use parse_character instead.
"""

import re
import itertools
from os import path, walk
from pathlib import Path
from npc import character
from npc.util import print_err

VALID_EXTENSIONS = ('.nwod', '.dnd3', '.dfrpg')
"""tuple: file extensions that should be parsed"""

DEPRECATED_TAGS = ('hidegroup', 'hideranks')

SECTION_RE = re.compile(r'^--.+--\s*$')
TAG_RE = re.compile(r'^@(?P<tag>#\w+|\w+)\s+(?P<value>.*)$')
HIDE_RE = re.compile(r'\s*>>\s*')

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
            extension in addition to recognized files.

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

def _walk_ignore(root: str, ignore):
    """
    Recursively traverse a directory tree while ignoring certain paths.

    Args:
        root (str): Directory to start at
        ignore (list): Paths to skip over

    Yields:
        A tuple (path, [dirs], [files]) as from `os.walk`.
    """
    def should_search(base: str, check: str) -> bool:
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

def parse_character(char_file_path) -> character.Character:
    """
    Parse a single character file

    Args:
        char_file_path (str): Path to the character file to parse

    Returns:
        Character object. Most keys store a list of values from the character.
        The string keys store a simple string, and the `rank` key stores
        a dict of list entries. Those keys are individual group names.
    """

    # derive character name from basename
    basename = path.basename(char_file_path)
    name = path.splitext(basename)[0].split(' - ', 1)[0]

    # instantiate new character
    parsed_char = character.Character(
        name=[name],
        path=char_file_path
    )

    with open(char_file_path, 'r') as char_file:
        subtag_registry = {}
        previous_line_empty = False

        for line in char_file:
            # stop processing once we see game stats
            if SECTION_RE.match(line):
                break

            match = TAG_RE.match(line)
            if match:
                tag = match.group('tag').lower()
                value = match.group('value')

                # skip comment tags
                if tag[0] == '#':
                    continue

                # handle compound tags
                if tag == 'changeling':
                    # grab attributes from compound tag
                    bits = value.split(maxsplit=1)
                    parsed_char.tags('type').append('Changeling')
                    if len(bits):
                        parsed_char.tags('seeming').append(bits[0])
                    if len(bits) > 1:
                        parsed_char.tags('kith').append(bits[1])
                    continue
                elif tag == 'werewolf':
                    parsed_char.tags('type').append('Werewolf')
                    parsed_char.tags('auspice').append(value)
                    continue

                # replace first name
                if tag == 'realname':
                    parsed_char.tags('name')[0] = value
                    continue

                # handle rank logic for group tags
                if parsed_char.tags(tag).subtag_name:
                    subtag_registry[parsed_char.tags(tag).subtag_name] = (tag, value)
                if tag in subtag_registry:
                    supertag, supervalue = subtag_registry[tag]
                    parsed_char.tags(supertag)[supervalue].append(value)
                    continue

                # mark tags hidden as needed
                if tag == 'hide':
                    parts = HIDE_RE.split(value)

                    tagname = parts.pop(0)
                    if not parts:
                        parsed_char.tags(tagname).hidden = True
                        continue

                    first_value = parts.pop(0)
                    if not parts:
                        parsed_char.tags(tagname).hide_value(first_value)
                        continue

                    second_value = parts.pop(0)
                    if not parts:
                        if second_value == 'subtags':
                            parsed_char.tags(tagname).subtag(first_value).hidden = True
                        else:
                            parsed_char.tags(tagname).subtag(first_value).hide_value(second_value)
                        continue

                    # If we can't parse the hide string, hide the whole thing as
                    # a tag and let the Character object deal with it.
                    parsed_char.tags(value).hidden = True
                    continue

                if tag in DEPRECATED_TAGS:
                    print_err("The tag '{}' in `{}` is deprecated and will stop working in the future".format(tag, char_file_path))

                parsed_char.tags(tag).append(value)
            else:
                # Ignore second empty description line in a row
                if line == "\n":
                    if previous_line_empty:
                        continue
                    else:
                        previous_line_empty = True
                else:
                    previous_line_empty = False

                # all remaining text goes in the description
                parsed_char.tags('description').append(line.strip())
                continue

    return character.build(other_char=parsed_char)
