
from os import walk
from pathlib import Path
from contextlib import contextmanager
import sys

from npc.character import Character
from npc import settings, util
from . import character_sorter

def create_path_from_character(character: Character, *, base_path=None, hierarchy=None, **kwargs):
    """
    Determine the best file path for a character.

    The path is created underneath base_path. It only includes directories
    which already exist. It's used by character creation, linting, and reorg.
    Its behavior is controlled by the hierarchy parameter.

    Args:
        character: Parsed character data
        base_path (str): Base path for character files
        hierarchy (str): Path spec defining which folders to create
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Constructed file path based on the character data.

    hierarchy Format
    ================

    The hierarchy argument is a string made up of one or more path components
    separated by a '/' character. Each component can either be a collection of
    characters or a tag substitution. Literal characters are inserted without
    being changed, as long as that folder already exists:

        create_path_from_character(..., hierarchy="Awesome/Heroes")

    This will attempt to add two folders to the constructed path, "Awesome" and
    then "Heroes".

    Substitutions are surrounded by {curly braces} and can either name a tag, or
    be a conditional. Conditionals check whether the character has data for the
    named tag, then inserts the second part of the substitution literally:

        create_path_from_character(..., hierarchy="{school?Student}")

    This will check if the character has data in its "school" tag, and if it
    does, attempt to add the "Student" folder to the constructed path.

        create_path_from_character(..., hierarchy="{school}")

    On the other hand, this will attempt to add a folder with the same name as
    the first value for "school" that the character has. So a character whose
    first school is "Middleton High" will make the function try to add a folder
    named "Middleton High" to the path.

    Alorithm summary
    ================

    * iterate through components of the hierarchy
    * anything not inside {curly braces} is inserted literally
    * everything else is interpreted

    conditionals:
        * check for '?' operator
        *   translate tag name if needed
        *   test tag presence
        *       most tags: has_tag(tag)
        *       foreign: foreign or wanderer
        *       type: not 'Unknown'
        *       *+ranks: any ranks exist
        *   if character has that tag, insert the literal
    tags:
        * translate tag name if needed
        * if the character has that tag:
        *   type: get 'types.type_key.type_path'
        *   group: use only the first group
        *   rank(s): iterate first group's ranks and add folders
        *   groups: iterate group value in order, trying to add a new path
        *       component for each
        *   groups+ranks: iterate group values, add folder, iterate that group's
        *       ranks and add folders
        *   locations: inserts first location, then first foreign
        *   all other tags: insert their first value
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    if not base_path:
        base_path = prefs.get('paths.required.characters')
    if not hierarchy:
        hierarchy = prefs.get('paths.hierarchy')

    target_path = Path(base_path)

    def add_path_if_exists(base, potential):
        """Add a directory to the base path if that directory exists."""
        test_path = base.joinpath(potential)
        if test_path.exists():
            return test_path
        return base

    def placeholder(component):
        return prefs.get(
            'types.{char_type}.missing_values.{component}'.format(
                char_type=character.type_key,
                component=component),
            '')

    for component in hierarchy.split('/'):
        if not(component.startswith('{') and component.endswith('}')):
            # No processing needed. Insert the literal and move on.
            target_path = add_path_if_exists(target_path, component)
            continue

        component = component.strip('{}')

        if '?' in component:
            tag_name, literal = component.split('?')
            tag_name = prefs.translate_tag_for_character_type(character.type_key, tag_name)
            if tag_name == 'foreign':
                # "foreign?" gets special handling to check the wanderer tag as well
                if character.foreign:
                    target_path = add_path_if_exists(target_path, literal)
            elif character.tags(tag_name).present:
                target_path = add_path_if_exists(target_path, literal)
            continue

        tag_name = prefs.translate_tag_for_character_type(character.type_key, component)
        if tag_name == 'type':
            # get the translated type path for the character's type
            target_path = add_path_if_exists(target_path, prefs.get('types.{}.type_path'.format(character.type_key), placeholder('type')))
        elif tag_name == 'group':
            # get just the first group
            target_path = add_path_if_exists(target_path, character.tags('group').first_value())
        elif tag_name in ['rank', 'ranks']:
            # iterate all ranks for the first group and add each one as a folder
            val = character.tags('group').first_value()
            for rank in character.tags('group').subtag(val):
                target_path = add_path_if_exists(target_path, rank)
        elif tag_name == 'groups':
            # iterate all group values and try to add each one as a folder
            for group_name in character.tags('group'):
                target_path = add_path_if_exists(target_path, group_name)
        elif tag_name == 'groups+ranks':
            # Iterate all groups, add each as a folder, then iterate all ranks
            # for that group and add each of those as folders
            for group_name in character.tags('group'):
                target_path = add_path_if_exists(target_path, group_name)
                for rank in character.tags('group').subtag(group_name):
                    target_path = add_path_if_exists(target_path, rank)
        elif tag_name == 'locations':
            # use the first location entry, or foreign entry
            location_value = character.tags('location').first_value()
            if not location_value:
                location_value = placeholder('location')
            target_path = add_path_if_exists(target_path, location_value)

            foreign_value = character.tags('foreign').first_value()
            if not foreign_value:
                foreign_value = placeholder('foreign')
            target_path = add_path_if_exists(target_path, foreign_value)
        else:
            # every other tag gets to use its first value
            val = character.tags(tag_name).first_value()
            if not val:
                val = placeholder(tag_name)
            target_path = add_path_if_exists(target_path, val)

    return target_path

def find_empty_dirs(root):
    """
    Find empty directories under root

    Args:
        root (str): Starting path to search

    Yields:
        Path of empty directories under `root`
    """
    for dirpath, dirs, files in walk(root):
        if not dirs and not files:
            yield dirpath

@contextmanager
def smart_open(filename=None, binary=False):
    """
    Open a named file or stdout as appropriate.

    This function is designed to be used in a `with` block.

    Args:
        filename (str|None): Name of the file path to open. None and '-' mean
            stdout.
        binary (bool): If opening a file, whether to open it in bytes mode. If
            opening stdout, whether to get its buffer.

    Yields:
        File-like object.

        When filename is None or the dash character ('-'), this function will
        yield sys.stdout. When filename is a path, it will yield the open file
        for writing.

    """
    if filename and filename != '-':
        stream = open(filename, 'wb') if binary else open(filename, 'w')
    else:
        stream = sys.stdout.buffer if binary else sys.stdout

    try:
        yield stream
    finally:
        if stream is not sys.stdout:
            stream.close()
