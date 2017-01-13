"""
Individual command functions and their helpers

These functions handle the real work of NPC. They can be called on their own
without going through the CLI.
"""

import re
import json
import sys
from collections import Counter
from contextlib import contextmanager
from datetime import datetime
from os import path, walk, makedirs, rmdir, scandir, getcwd
from shutil import copy as shcopy, move as shmove
import itertools

# local packages
from . import formatters, linters, parser, settings
from .util import Result, Character, flatten

def create_changeling(name, seeming, kith, *,
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
    temp_char = Character()
    temp_char.append('type', 'changeling') \
             .append('seeming', seeming)   \
             .append('kith', kith)
    if court:
        temp_char.append('court', court.title())
    if motley:
        temp_char.append('motley', motley)
    if groups:
        temp_char['group'] = groups
    if dead:
        temp_char.append('dead', dead)
    if foreign:
        temp_char.append('foreign', foreign)

    # get path for the new file
    target_path = create_path_from_character(temp_char, prefs=prefs)

    filename = name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '{}' already exists!".format(name), errcode=1)

    # Create tags
    seeming_name = seeming.title()
    kith_name = kith.title()
    tags = ['@changeling {} {}'.format(seeming_name, kith_name)]
    if motley:
        tags.append('@motley {}'.format(motley))
    if court:
        tags.append('@court {}'.format(court.title()))
    tags.extend(_make_std_tags(groups=groups, dead=dead, foreign=foreign))

    header = prefs.get('template_header') + "\n".join(tags) + '\n\n'

    # Copy template data
    template_path = prefs.get('templates.changeling')
    try:
        with open(template_path, 'r') as template:
            data = header + template.read()
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(template_path), errcode=4)

    # insert seeming and kith in the advantages block
    sk_data = prefs.get('changeling')
    seeming_key = seeming.lower()
    if seeming_key in sk_data['seemings']:
        seeming_notes = "{}; {}".format(sk_data['blessings'][seeming_key], sk_data['curses'][seeming_key])
        data = seeming_re.sub(
            r"\g<1>Seeming\g<2>{} ({})".format(seeming_name, seeming_notes),
            data
        )
    kith_key = kith.lower()
    if kith_key in sk_data['kiths']:
        kith_notes = sk_data['blessings'][kith_key]
        data = kith_re.sub(
            r"\g<1>Kith\g<2>{} ({})".format(kith_name, kith_notes),
            data
        )

    # Save the new character
    try:
        with open(target_path, 'w') as target_file:
            target_file.write(data)
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(target_path), errcode=4)

    return Result(True, openable=[target_path])

def _make_std_tags(groups=None, dead=False, foreign=""):
    """
    Create standard tags that apply to all character types.

    Args:
        groups (list): One or more names of groups the character belongs to.
            Used to derive path.
        dead (bool|str): Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
        foreign (bool): Details of non-standard residence. Leave empty to
            exclude the @foreign tag.

    Returns:
        List of strings containing group, dead, and foreign tags.
    """
    if groups is None:
        groups = []

    tags = ["@group {}".format(g) for g in groups]
    if dead != False:
        dead_details = " {}".format(dead) if len(dead) else ""
        tags.append("@dead{}".format(dead_details))
    if foreign:
        tags.append("@foreign {}".format(foreign))
    return tags

def create_simple(name, ctype, *, dead=False, foreign=False, **kwargs):
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

    if ctype not in prefs.get('templates'):
        return Result(False, errmsg="Unrecognized template '{}'".format(ctype), errcode=7)

    # build minimal character
    temp_char = Character()
    temp_char.append('type', ctype)
    if groups:
        temp_char['group'] = groups
    if dead:
        temp_char.append('dead', dead)
    if foreign:
        temp_char.append('foreign', foreign)

    # get path for the new file
    target_path = create_path_from_character(temp_char, prefs=prefs)

    filename = name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '{}' already exists!".format(name), errcode=1)

    # Add tags
    typetag = ctype.title()
    tags = ['@type {}'.format(typetag)] + _make_std_tags(groups=groups, dead=dead, foreign=foreign)
    header = prefs.get('template_header') + "\n".join(tags) + '\n\n'

    # Copy template
    template = prefs.get('templates.{}'.format(ctype))
    try:
        with open(template, 'r') as template_data:
            data = header + template_data.read()
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(template), errcode=4)

    # Write the new file
    try:
        with open(target_path, 'w') as char_file:
            char_file.write(data)
    except IOError as err:
        return Result(False, errmsg=err.strerror + " ({})".format(target_path), errcode=4)

    return Result(True, openable=[target_path])

def session(**kwargs):
    """
    Create the files for a new game session.

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log.

    Args:
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the current and previous session
        log and plot planning files.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    plot_path = prefs.get('paths.plot')
    session_path = prefs.get('paths.session')

    if not (path.exists(plot_path) and path.exists(session_path)):
        return Result(False, errmsg="Cannot access paths '{}' and/or '{}'".format(plot_path, session_path), errcode=4)

    plot_re = re.compile(r'(?i)^plot (?P<number>\d+)$')
    session_re = re.compile(r'(?i)^session (?P<number>\d+)$')

    def get_latest(target_path, target_regex):
        """Get the "latest" file in target_path that matches target_regex"""
        buncha_files = [f.name for f in scandir(target_path) if f.is_file() and target_regex.match(path.splitext(f.name)[0])]
        try:
            latest_file = max(buncha_files, key=lambda f: re.split(r'\s', f)[1])
            (bare_name, bare_ext) = path.splitext(latest_file)
            file_match = target_regex.match(bare_name)
            file_number = int(file_match.group('number'))
        except ValueError:
            latest_file = ''
            bare_ext = '.md'
            file_number = 0

        return {
            'name': latest_file,
            'ext': bare_ext,
            'number': file_number,
            'path': path.join(target_path, latest_file),
            'exists': file_number > 0
        }

    # find latest plot and session file
    latest_plot = get_latest(plot_path, plot_re)
    latest_session = get_latest(session_path, session_re)

    new_number = min(latest_plot['number'], latest_session['number']) + 1

    openable = []
    if latest_session['exists']:
        if latest_session['number'] < new_number:
            # create new session log
            old_session_path = latest_session['path']
            new_session_path = path.join(session_path, "session {num}{ext}".format(num=new_number, ext=latest_session['ext']))
            shcopy(prefs.get('templates.session'), new_session_path)
        else:
            # present existing session files, since we don't have to create one
            old_session_path = path.join(session_path, "session {num}{ext}".format(num=latest_session['number'] - 1, ext=latest_session['ext']))
            new_session_path = latest_session['path']
        openable.extend((new_session_path, old_session_path))
    else:
        # no existing session, so just copy the template
        template_path = prefs.get('templates.session')
        new_session_path = path.join(session_path, "session {num}{ext}".format(num=new_number, ext=path.splitext(template_path)[1]))
        shcopy(template_path, new_session_path)
        openable.append(new_session_path)

    if latest_plot['exists']:
        if latest_plot['number'] < new_number:
            # copy old plot
            old_plot_path = latest_plot['path']
            new_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=new_number, ext=latest_plot['ext']))
            shcopy(old_plot_path, new_plot_path)
        else:
            # present existing plot files, since we don't have to create one
            old_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=latest_plot['number'] - 1, ext=latest_plot['ext']))
            new_plot_path = latest_plot['path']
        openable.extend((new_plot_path, old_plot_path))
    else:
        # no old plot to copy, so create a blank
        new_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=new_number, ext=prefs.get('plot_ext')))
        with open(new_plot_path, 'w') as new_plot:
            new_plot.write(' ')
        openable.append(new_plot_path)

    return Result(True, openable=openable)

def reorg(*search, ignore=None, purge=False, verbose=False, dryrun=False, **kwargs):
    """
    Move character files into the correct paths.

    Character files are moved so that their path matches the ideal path as
    closely as possible. No new directories are created.

    Args:
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        purge (bool): Whether empty directories should be deleted after all
            files have been moved.
        verbose (bool): Whether to print changes as they are made
        dryrun (bool): Whether to show the changes that would be made, but not
            enact them.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will be empty.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get('paths.ignore'))
    verbose = verbose or dryrun

    changelog = []

    base_path = prefs.get('paths.characters')
    if not path.exists(base_path):
        return Result(False, errmsg="Cannot access '{}'".format(base_path), errcode=4)

    for parsed_character in parser.get_characters(flatten(search), ignore):
        new_path = create_path_from_character(parsed_character, target_path=base_path)
        if new_path != path.dirname(parsed_character['path']):
            if verbose:
                changelog.append("Moving {} to {}".format(parsed_character['path'], new_path))
            if not dryrun:
                shmove(parsed_character['path'], new_path)

    if purge:
        for empty_path in find_empty_dirs(base_path):
            if verbose:
                changelog.append("Removing empty directory {}".format(empty_path))
            if not dryrun:
                rmdir(empty_path)

    return Result(True, printable=changelog)

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

def create_path_from_character(character: Character, *, target_path=None, **kwargs):
    """
    Determine the best file path for a character.

    The path is created underneath target_path. It only includes directories
    which already exist.

    Args:
        character: Parsed character data
        target_path (str): Base path for character files
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Constructed file path based on the character data.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    if not target_path:
        target_path = prefs.get('paths.characters')

    # add type-based directory if we can
    ctype = character.type_key
    if ctype:
        target_path = _add_path_if_exists(target_path, prefs.get('type_paths.{}'.format(ctype), '.'))
    else:
        ctype = 'none'

    # handle type-specific considerations
    if ctype == 'changeling':
        # changelings use court first, then groups
        if 'court' in character:
            for court_name in character['court']:
                target_path = _add_path_if_exists(target_path, court_name)
        else:
            target_path = _add_path_if_exists(target_path, 'Courtless')

    # foreigners get a special folder
    if 'foreign' in character or 'wanderer' in character:
        target_path = _add_path_if_exists(target_path, 'Foreign')

    # everyone uses groups in their path
    if 'group' in character:
        for group_name in character['group']:
            target_path = _add_path_if_exists(target_path, group_name)

    return target_path

def _add_path_if_exists(base, potential):
    """Add a directory to the base path if that directory exists."""
    test_path = path.join(base, potential)
    if path.exists(test_path):
        return test_path
    return base

def listing(*search, ignore=None, fmt=None, metadata=None, title=None, outfile=None, **kwargs):
    """
    Generate a listing of NPCs.

    Args:
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        fmt (str): Format of the output. Supported types are 'markdown', 'md',
            'htm', 'html', and 'json'. Pass 'default' or None to get format from
            settings.
        metadata (str|None): Whether to include metadata in the output and what
            kind of metadata to use. Pass 'default' to use the format configured
            in Settings.

            The markdown format allows either 'mmd' (MultiMarkdown) or
            'yfm'/'yaml' (Yaml Front Matter) metadata.

            The json format only allows one form of metadata, so pass any truthy
            value to include the metadata keys.
        title (str|None): The title to put in the metadata, if included.
            Overrides the title from settings.
        outfile (string|None): Filename to put the listed data. None and "-"
            print to stdout.
        sort (string|None): Sort order for characters. Defaults to the value of
            "list_sort" in settings.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the output file if given.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get('paths.ignore'))
    sort_order = kwargs.get('sort', prefs.get('list_sort'))

    characters = _sort_chars(
        _prune_chars(parser.get_characters(flatten(search), ignore)),
        order=sort_order)

    if fmt == "default" or not fmt:
        fmt = prefs.get('list_format')
    out_type = formatters.get_canonical_format_name(fmt)

    dumper = formatters.get_listing_formatter(out_type)
    if not dumper:
        return Result(False, errmsg="Cannot create output of format '{}'".format(out_type), errcode=5)

    if metadata == 'default' and out_type != 'json':
        # Ensure 'default' metadata type gets replaced with the right default
        # metadata format. Irrelevant for json format.
        metadata_type = prefs.get('metadata.default_format.{}'.format(out_type))
    else:
        metadata_type = metadata

    meta = prefs.get_metadata(out_type)
    if title:
        meta['title'] = title

    with _smart_open(outfile, binary=(out_type in formatters.BINARY_TYPES)) as outstream:
        response = dumper(
            characters,
            outstream,
            include_metadata=metadata_type,
            metadata=meta,
            prefs=prefs,
            sectioner=_get_sectioner(sort_order))

    # pass errors straight through
    if not response.success:
        return response

    openable = [outfile] if outfile and outfile != '-' else None

    return Result(True, openable=openable)

def _sort_chars(characters, order=None):
    """
    Sort a list of Characters.

    Args:
        characters (list): Characters to sort. Defaults to "last".
        order (str): The order in which the characters should be sorted.
            Unrecognized sort orders are ignored. Supported orders are:
            * "last" - sort by last-most name
            * "first" - sort by first name

    Returns:
        List of characters ordered as requested.
    """
    def last_name(character):
        """Get the character's last-most name"""
        return character.get_first('name').split(' ')[-1]

    def first_name(character):
        """Get the character's first name"""
        return character.get_first('name').split(' ')[0]

    if not order or order == "last":
        return sorted(characters, key=last_name)
    if order == "first":
        return sorted(characters, key=first_name)
    return characters

def _get_sectioner(order):
    """
    Get a sectioning function

    Args:
        order (str): Name of the order that defines the sections. One of "last"
            or "first"

    Returns:
        A sectioning function, or None if the order was not recognized
    """
    def first_letter_last_name(character):
        """Get the first letter of the character's last-most name"""
        return character.get_first('name').split(' ')[-1][0]

    def first_letter_first_name(character):
        """Get the first letter of the character's first name"""
        return character.get_first('name').split(' ')[0][0]

    if order == 'first':
        return first_letter_first_name
    if order == 'last':
        return first_letter_last_name
    return None

def _prune_chars(characters):
    """
    Alter character records for output.

    This applies behavior from directives and certain tags:

    * skip: remove the character from the list
    * hide: remove the named fields from the character
    * hidegroup: remove the named group from the character
    * hideranks: remove the character's ranks in the named group
    * faketype: replace the character's type with a new string

    It also inserts a placeholder type if one was not specified.

    Args:
        characters (list): List of Character objects

    Yields:
        Modified Character objects
    """

    for char in characters:
        # skip if asked
        if 'skip' in char:
            continue

        # remove named fields
        for fieldname in char['hide']:
            if fieldname in char:
                del char[fieldname]

        # remove named groups
        for groupname in char['hidegroup']:
            char['group'].remove(groupname)

        # remove all ranks for named groups
        for groupname in char['hideranks']:
            if groupname in char['rank']:
                del char['rank'][groupname]

        # use fake types if present
        if 'faketype' in char:
            char['type'] = char['faketype']

        # Use a placeholder for unknown type
        if 'type' not in char:
            char['type'] = 'Unknown'

        yield char

@contextmanager
def _smart_open(filename=None, binary=False):
    """
    Open a named file or stdout as appropriate.

    This method is designed to be used in a `with` block.

    Args:
        filename (str|None): Name of the file path to open. None and '-' mean
            stdout.
        binary (bool): If opening a file, whether to open it in bytes mode. If
            opening stdout, whether to get its buffer.

    Yields:
        File-like object.

        When filename is None or the dash character ('-'), this method will
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

def dump(*search, ignore=None, sort=False, metadata=False, outfile=None, **kwargs):
    """
    Dump the raw character data, unaltered.

    Always formats the data as json.

    Args:
        search (List): Paths to search for character files
        ignore (List): Paths to ignore
        sort (bool): Whether to sort the characters before dumping
        metadata (bool): Whether to prepend metadata to the output
        outfile (string|None): Filename to put the dumped data. None and "-"
            print to stdout.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. If outfile pointed to a real file, the openable attribute
        will contain that filename.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get('paths.ignore'))

    characters = parser.get_characters(flatten(search), ignore)
    if sort:
        characters = _sort_chars(characters)

    # make some json
    if metadata:
        meta = {
            'meta': True,
            **prefs.get_metadata('json')
        }
        characters = itertools.chain([meta], characters)

    with _smart_open(outfile) as outstream:
        json.dump([c for c in characters], outstream)

    openable = [outfile] if outfile and outfile != '-' else None

    return Result(True, openable=openable)

def lint(*search, ignore=None, fix=False, strict=False, **kwargs):
    """
    Check character files for completeness and correctness.

    This method checks that every character file has a few required tags, and
    applies extra checking for some character types. See util.Character.validate
    for details.

    Args:
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        fix (bool): Whether to automatically fix errors when possible
        strict (bool): Whether to report non-critical errors and omissions
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. On success, openable attribute will contain a list of all
        files that had errors.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get('paths.ignore'))

    openable = []

    # check each character
    characters = parser.get_characters(flatten(search), ignore)
    for character in characters:
        character.validate(strict)
        character.problems.extend(linters.lint(character, fix=fix, strict=strict, prefs=prefs))

        # Report problems on one line if possible, or as a block if there's more than one
        if not character.valid:
            openable.append(character['path'])
            if len(character.problems) > 1:
                print("File '{}':".format(character['path']))
                for detail in character.problems:
                    print("    {}".format(detail))
            else:
                print("{} in '{}'".format(character.problems[0], character['path']))

    return Result(True, openable=openable)

def init(create_types=False, create_all=False, **kwargs):
    """
    Create the basic directories for a campaign.

    This will create the directories this tool expects to find within a
    campaign. Other directories are left to the user.

    Args:
        create_types (bool): Whether to create directories for each character
            type
        create_all (bool): Whether to create all optional directories.
        campaign_name (str): Name of the campaign. Defaults to the name of the
            current directory.
        dryrun (bool): Do not create anything. This adds a string of changes
            that would be made to the returned Result object's printable
            variable.
        verbose (bool): Detail all changes made in the Result object's printable
            variable.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will be empty.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    campaign_name = kwargs.get('campaign_name', path.basename(getcwd()))
    dryrun = kwargs.get('dryrun', False)
    verbose = kwargs.get('verbose', False)

    changelog = []

    def log_change(message):
        if dryrun or verbose:
            changelog.append(message)

    def new_dir(path_name):
        log_change(path_name)
        if not dryrun:
            makedirs(path_name, mode=0o775, exist_ok=True)

    for key, basic_path in prefs.get('paths').items():
        if key == "ignore":
            continue
        new_dir(basic_path)
    if not path.exists(prefs.get_settings_path('campaign')):
        new_dir('.npc')
        log_change(prefs.get_settings_path('campaign'))
        if not dryrun:
            with open(prefs.get_settings_path('campaign'), 'a') as settings_file:
                json.dump({'campaign': campaign_name}, settings_file, indent=4)

    if create_types or create_all:
        cbase = prefs.get('paths.characters')
        for _, type_path in prefs.get('type_paths').items():
            new_dir(path.join(cbase, type_path))

    return Result(True, printable=changelog)

def open_settings(location, show_defaults=False, settings_type=None, **kwargs):
    """
    Open the named settings file.

    If the desired settings file does not exist, an empty file is created and
    then opened.

    Args:
        location (str): Which settings file to open. One of 'user' or 'campaign'.
        show_defaults (bool): Whether the default settings file should be opened
            for reference alongside the specified settings file.
        settings_type (str): Determines which kind of settings file to open,
            like base settings or changeling settings. If left unset, base
            settings are opened. One of 'base' or 'changeling'.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the desired settings file. If true
        was passed in show_defaults, it will also contain the reference settings
        file.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if settings_type:
        settings_type = settings_type.lower()

    target_path = prefs.get_settings_path(location, settings_type)
    if not path.exists(target_path):
        dirname = path.dirname(target_path)
        makedirs(dirname, mode=0o775, exist_ok=True)
        with open(target_path, 'a') as settings_file:
            settings_file.write('{}')

    if show_defaults:
        openable = [prefs.get_settings_path('default', settings_type), target_path]
    else:
        openable = [target_path]
    return Result(True, openable=openable)

def report(*tags, search=None, ignore=None, fmt=None, outfile=None, **kwargs):
    """
    Create a report for the given tags

    The tabular report shows how many characters have each unique value for each
    tag.

    Args:
        tag (list): Tag names to report on. Can contain strings and lists of
            strings.
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        fmt (str|None): Output format to use. Recognized values are defined in
            formatters.get_report_formatter. Pass "default" or None to get the
            format from settings.
        outfile (string|None): Filename to put the listed data. None and "-"
            print to stdout.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the output file if given.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    if not ignore:
        ignore = []
    ignore.extend(prefs.get('paths.ignore'))
    if not fmt or fmt == 'default':
        fmt = prefs.get('report_format')

    # use a list so we can iterate more than once
    characters = list(parser.get_characters(flatten(search), ignore))

    # Construct a dict keyed by tag name whose values are Counters. Each Counter
    # is initialized with a flattened list of lists and we let it count the
    # duplicates.
    table_data = {tag : Counter(flatten([c.get(tag, 'None') for c in characters])) for tag in flatten(tags)}

    outputter = formatters.get_report_formatter(fmt)
    if not outputter:
        return Result(False, errmsg="Cannot create output of format '{}'".format(fmt), errcode=5)
    with _smart_open(outfile, binary=(fmt in formatters.BINARY_TYPES)) as outstream:
        response = outputter(table_data, outstream=outstream, prefs=prefs)

    # pass errors straight through
    if not response.success:
        return response

    openable = [outfile] if outfile and outfile != '-' else None

    return Result(True, openable=openable)
