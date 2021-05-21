"""
Functions for creating new character sheets
"""

import re

from npc import settings, character
from npc.util import result, print_err

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
        foreign (bool|str): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        location (str): Details about where the character lives. Leave empty to
            exclude the @location tag.
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the new character file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    groups = kwargs.get('groups', [])
    location = kwargs.get('location', False)
    ctype = ctype.lower()

    if not prefs.get("types.{}.sheet_template".format(ctype)):
        return result.ConfigError(errmsg="Character type '{}' does not have a sheet template".format(ctype))

    # build minimal character
    temp_char = _minimal_character(
        ctype=ctype,
        groups=groups,
        dead=dead,
        foreign=foreign,
        location=location,
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
        foreign (bool|str): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        location (str): Details about where the character lives. Leave empty to
            exclude the @location tag.
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        freehold (str): Name of the freehold the changeling belongs to. Leave
            empty to exclude @freehold tag.
        entitlement (str): Name of the entitlement the changeling belongs to.
            Leave empty to exclude @entitlement tag.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the path to the new character file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    groups = kwargs.get('groups', [])
    location = kwargs.get('location', False)
    freehold = kwargs.get('freehold', None)
    entitlement = kwargs.get('entitlement', None)

    # build minimal Character
    temp_char = _minimal_character(
        ctype='changeling',
        groups=groups,
        dead=dead,
        foreign=foreign,
        location=location,
        prefs=prefs)
    temp_char.tags('seeming').append(seeming.title())
    temp_char.tags('kith').append(kith.title())
    if court:
        temp_char.tags('court').append(court.title())
    if motley:
        temp_char.tags('motley').append(motley)
    if freehold:
        temp_char.tags('freehold').append(freehold)
    if entitlement:
        temp_char.tags('entitlement').append(entitlement)

    def _insert_sk_data(data):
        """Insert seeming and kith in the advantages block of a template"""

        seeming_re = re.compile(
            r'^(\s+)seeming(\s+)\w+$',
            re.MULTILINE | re.IGNORECASE
        )
        kith_re = re.compile(
            r'^(\s+)kith(\s+)\w+$',
            re.MULTILINE | re.IGNORECASE
        )

        seeming_name = temp_char.tags('seeming').first_value()
        seeming_key = seeming.lower()
        if seeming_key in prefs.get('changeling.seemings'):
            seeming_notes = "{}; {}".format(
                prefs.get("changeling.blessings.{}".format(seeming_key)),
                prefs.get("changeling.curses.{}".format(seeming_key)))
            data = seeming_re.sub(
                r"\g<1>Seeming\g<2>{} ({})".format(seeming_name, seeming_notes),
                data
            )
        else:
            print_err("Unrecognized seeming '{}'".format(seeming_name))

        kith_name = temp_char.tags('kith').first_value()
        kith_key = kith.lower()
        if kith_key in prefs.get('changeling.kiths.{}'.format(seeming_key), []):
            kith_notes = prefs.get("changeling.blessings.{}".format(kith_key))
            data = kith_re.sub(
                r"\g<1>Kith\g<2>{} ({})".format(kith_name, kith_notes),
                data
            )
        else:
            print_err("Unrecognized kith '{}' for seeming '{}'".format(kith_name, seeming_name))

        return data

    return _cp_template_for_char(name, temp_char, prefs, fn=_insert_sk_data)

def werewolf(name, auspice, *, tribe=None, pack=None, **kwargs):
    """
    Create a Werewolf character.

    Args:
        name (str): Base file name
        auspice (str): Name of the character's Auspice.
        tribe (str): Name of the character's Tribe. Leave empty for Ghost Wolves.
        pack (str): name of the character's pack.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool|str): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        location (str): Details about where the character lives. Leave empty to
            exclude the @location tag.
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the path to the new character file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    groups = kwargs.get('groups', [])
    location = kwargs.get('location', False)
    dead = kwargs.get('dead', False)
    foreign = kwargs.get('foreign', False)

    # build minimal Character
    temp_char = _minimal_character(
        ctype='werewolf',
        groups=groups,
        dead=dead,
        foreign=foreign,
        location=location,
        prefs=prefs)
    temp_char.tags('auspice').append(auspice.title())
    if tribe:
        temp_char.tags('tribe').append(tribe.title())
    if pack:
        temp_char.tags('pack').append(pack)

    return _cp_template_for_char(name, temp_char, prefs)

def _minimal_character(ctype: str, groups: list, dead, foreign, location, prefs):
    """
    Create a minimal character object

    Args:
        ctype (str): Character type
        groups (list): One or more names of groups the character belongs to.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool|str): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.
        location (str): Details about where the character lives. Leave empty to
            exclude the @location tag.
        prefs (Settings): Settings object

    Returns:
        Character object
    """
    attributes = prefs.get('tag_defaults')
    attributes['description'] = [prefs.get('character_header')]
    attributes['type'] = [ctype.title()]
    if groups:
        attributes['group'] = groups
    if dead is not False:
        if dead is True:
            dead = ''
        attributes['dead'] = dead
    if foreign is not False:
        attributes['foreign'] = foreign
    if location is not False:
        attributes['location'] = location

    return character.build(attributes=attributes)

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
    template_path = prefs.get('types.{}.sheet_template'.format(character.type_key))
    if not template_path:
        return result.ConfigError(errmsg="Could not find template {}".format(character.type_key))

    # get path for the new file
    target_path = create_path_from_character(character, prefs=prefs)

    filename = name + template_path.suffix
    target_path = target_path.joinpath(filename)
    if target_path.exists():
        return result.FSError(errmsg="Character '{}' already exists!".format(name))

    # Add tags
    header = '\n\n' + character.build_header() + '\n\n'

    # Copy template
    try:
        with open(template_path, 'r') as template_data:
            data = header + template_data.read()
    except IOError as err:
        return result.FSError(errmsg=err.strerror + " ({})".format(template_path))

    if callable(fn):
        data = fn(data)

    # Write the new file
    try:
        with open(target_path, 'w') as char_file:
            char_file.write(data)
    except IOError as err:
        return result.FSError(errmsg=err.strerror + " ({})".format(target_path))

    return result.Success(openable=[target_path])
