"""
Functions for creating new character sheets
"""

import re
from os import path

from npc import settings
from npc.util import Result
from npc.character import Character

from .util import create_path_from_character

def standard(name, ctype, *, dead=False, foreign=False, **kwargs):
    """
    Create a character without extra processing.

    Simple characters don't have any unique tags or file annotations. Everything
    is based on their type.

    Args:
        name (str): Base file name. Format is "<character name> - <brief note>".
        ctype (str): Character type. Must have a template configured in prefs.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the new character file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    groups = kwargs.get('groups', [])
    ctype = ctype.lower()

    if ctype not in prefs.get('templates'):
        return Result(False, errmsg="Unrecognized template '{}'".format(ctype), errcode=7)

    # build minimal character
    temp_char = _minimal_character(
        ctype=ctype.title(),
        groups=groups,
        dead=dead,
        foreign=foreign,
        prefs=prefs)

    return _cp_template_for_char(name, temp_char, prefs)

def changeling(name, seeming, kith, *,
                      court=None, motley=None, dead=False, foreign=False, **kwargs):
    """
    Create a Changeling character.

    Args:
        name (str): Base file name
        seeming (str): Name of the character's Seeming. Added to the file with
            notes.
        kith (str): Name of the character's Kith. Added to the file with notes.
        court (str|none): Name of the character's Court. Used to derive path.
        motley (str|none): Name of the character's Motley.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the path to the new character file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    groups = kwargs.get('groups', [])

    seeming_re = re.compile(
        r'^(\s+)seeming(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        r'^(\s+)kith(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )

    # build minimal Character
    temp_char = _minimal_character(
        ctype='changeling',
        groups=groups,
        dead=dead,
        foreign=foreign,
        prefs=prefs)
    temp_char.append('seeming', seeming.title())
    temp_char.append('kith', kith.title())
    if court:
        temp_char.append('court', court.title())
    if motley:
        temp_char.append('motley', motley)

    def _insert_sk_data(data):
        """Insert seeming and kith in the advantages block of a template"""
        seeming_name = temp_char.get_first('seeming')
        seeming_key = seeming.lower()
        if seeming_key in prefs.get('changeling.seemings'):
            seeming_notes = "{}; {}".format(
                prefs.get("changeling.blessings.{}".format(seeming_key)),
                prefs.get("changeling.curses.{}".format(seeming_key)))
            data = seeming_re.sub(
                r"\g<1>Seeming\g<2>{} ({})".format(seeming_name, seeming_notes),
                data
            )
        kith_name = temp_char.get_first('kith')
        kith_key = kith.lower()
        if kith_key in prefs.get('changeling.kiths.{}'.format(seeming_key)):
            kith_notes = prefs.get("changeling.blessings.{}".format(kith_key))
            data = kith_re.sub(
                r"\g<1>Kith\g<2>{} ({})".format(kith_name, kith_notes),
                data
            )
        return data

    return _cp_template_for_char(name, temp_char, prefs, fn=_insert_sk_data)

def _minimal_character(ctype, groups, dead, foreign, prefs):
    """
    Create a minimal character object

    Args:
        ctype (str): Character type
        groups (list): One or more names of groups the character belongs to.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        prefs (Settings): Settings object

    Returns:
        Character object
    """
    temp_char = Character()
    temp_char.append('description', prefs.get('template_header'))
    temp_char.append('type', ctype.title())
    if groups:
        temp_char['group'] = groups
    if dead is not False:
        temp_char.append('dead', dead)
    if foreign is not False:
        temp_char.append('foreign', foreign)

    return temp_char

def _cp_template_for_char(name, character, prefs, fn=None):
    """
    Copy the template for a character

    Copies the configured template file for `character` and optionally modifies
    the template's body using `fn`.

    Args:
        name (str): Character name
        character (Character): Character that needs a template
        prefs (Settings): Settings object used to find the template
        fn (callable): Optional function that is called before the new file is
            saved. It must accept a single string argument which will contain
            the template contents.

    Returns:
        Result object. Openable will contain the path to the new character file.
    """
    # get template path
    template_path = prefs.get('templates.{}'.format(character.type_key))
    if not template_path:
        return Result(False, errmsg="Could not find template {}".format(character.type_key), errcode=7)

    # get path for the new file
    target_path = create_path_from_character(character, prefs=prefs)

    filename = name + path.splitext(template_path)[1]
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '{}' already exists!".format(name), errcode=1)

    # Add tags
    header = character.build_header() + '\n\n'

    # Copy template
    try:
        with open(template_path, 'r') as template_data:
            data = header + template_data.read()
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(template_path), errcode=4)

    if callable(fn):
        data = fn(data)

    # Write the new file
    try:
        with open(target_path, 'w') as char_file:
            char_file.write(data)
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(target_path), errcode=4)

    return Result(True, openable=[target_path])