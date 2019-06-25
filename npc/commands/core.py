"""
Package for command functions and their helpers

These functions handle the real work of NPC. They can be called on their own
without going through the CLI.
"""

import json
from collections import Counter
from os import makedirs, rmdir, getcwd
from pathlib import Path
from shutil import move as shmove
import itertools

import npc
from npc import formatters, linters, parser, settings
from npc.util import flatten, result
from npc.character import Character, CharacterEncoder

from . import create_character, listing, util, story

def reorg(*search, ignore=None, purge=False, verbose=False, commit=False, **kwargs):
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
        commit (bool): Whether to actually move files around
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will be empty.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get_ignored_paths('reorg'))
    show_changes = verbose or not commit

    changelog = []

    base_path = Path(prefs.get('paths.required.characters'))
    if not base_path.exists():
        return result.FSError(errmsg="Cannot access '{}'".format(base_path))

    if show_changes:
        changelog.append("Move characters")
    for parsed_character in parser.get_characters(flatten(search), ignore):
        if parsed_character.tags('keep').present:
            continue
        new_path = Path(util.create_path_from_character(parsed_character, base_path=base_path))
        parsed_path = Path(parsed_character.path)
        if not new_path.resolve().samefile(parsed_path.resolve()):
            if show_changes:
                changelog.append("* Move {} to {}".format(parsed_path, new_path))
            if commit:
                try:
                    shmove(str(parsed_path), new_path)
                except OSError as e:
                    if show_changes:
                        changelog.append("\t- dest path already exists; skipping")

    if purge:
        if show_changes:
            changelog.append("Purge empty directories")
        for empty_path in util.find_empty_dirs(base_path):
            if show_changes:
                changelog.append("* Remove empty directory {}".format(empty_path))
            if commit:
                rmdir(empty_path)

    return result.Success(printables=changelog)

def dump(*search, ignore=None, do_sort=False, metadata=False, outfile=None, **kwargs):
    """
    Dump the raw character data, unaltered.

    Always formats the data as json.

    Args:
        search (List): Paths to search for character files
        ignore (List): Paths to ignore
        do_sort (bool): Whether to sort the characters before dumping
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
    ignore.extend(prefs.get_ignored_paths('dump'))
    sort_by = kwargs.get('sort_by', prefs.get('dump.sort_by'))

    characters = parser.get_characters(flatten(search), ignore)
    if do_sort:
        sorter = util.character_sorter.CharacterSorter(sort_by, prefs=prefs)
        characters = sorter.sort(characters)

    characters = [c.dump() for c in characters]

    # make some json
    if metadata:
        meta = {
            'meta': True,
            **prefs.get_metadata('json')
        }
        characters = itertools.chain([meta], characters)

    with util.smart_open(outfile) as outstream:
        json.dump([c for c in characters], outstream, cls=CharacterEncoder)

    openable = [outfile] if outfile and outfile != '-' else None

    return result.Success(openable=openable)

def lint(*search, ignore=None, fix=False, strict=False, report=True, **kwargs):
    """
    Check character files for completeness and correctness.

    This function checks that every character file has a few required tags, and
    applies extra checking for some character types. See util.Character.validate
    for details.

    This command normally ignores unknown tags. In strict mode, it will report
    the presence of any tag not expected by the character class.

    Args:
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        fix (bool): Whether to automatically fix errors when possible
        strict (bool): Whether to include non-critical errors and omissions
        report (bool): Do not include files in the return data, only problem
            descriptions
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. On success, openable attribute will contain a list of all
        files that had errors.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get_ignored_paths('lint'))

    openable = []
    printable = []

    # check each character
    characters = parser.get_characters(flatten(search), ignore)
    for character in characters:
        character.validate(strict)
        character.problems.extend(linters.lint(character, fix=fix, strict=strict, prefs=prefs))

        # Report problems on one line if possible, or as a block if there's more than one
        if not character.valid:
            charpath = character.path
            if not report:
                openable.append(charpath)
            if len(character.problems) > 1:
                printable.append("File '{}':".format(charpath))
                for detail in character.problems:
                    printable.append("    {}".format(detail))
            else:
                printable.append("{} in '{}'".format(character.problems[0], charpath))

    return result.Success(openable=openable, printables=printable)

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
            that would be made to the returned Result object's printables
            variable.
        verbose (bool): Detail all changes made in the Result object's
            printables variable.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will be empty.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    campaign_name = kwargs.get('campaign_name', Path.cwd().name)
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

    for key, required_path in prefs.get('paths.required').items():
        if key in ["additional_paths"]:
            # create user-specified dirs
            for extra_path in required_path:
                new_dir(extra_path)
            continue
        new_dir(required_path)
    if not prefs.get_settings_path('campaign').exists():
        new_dir('.npc')
        log_change(prefs.get_settings_path('campaign'))
        if not dryrun:
            with open(prefs.get_settings_path('campaign'), 'a') as settings_file:
                json.dump({'campaign_name': campaign_name}, settings_file, indent=4)

    if create_types or create_all:
        cbase = Path(prefs.get('paths.required.characters'))
        for type_path in prefs.get_type_paths():
            new_dir(cbase.joinpath(type_path))

    return result.Success(printables=changelog)

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
    if not target_path.exists():
        dirname = target_path.parent
        makedirs(dirname, mode=0o775, exist_ok=True)
        with open(target_path, 'a') as settings_file:
            settings_file.write('{}')

    if show_defaults:
        openable = [prefs.get_settings_path('default', settings_type, target_path.suffix), target_path]
    else:
        openable = [target_path]
    return result.Success(openable=openable)

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

    if not search:
        search = ['.']
    if not ignore:
        ignore = []
    ignore.extend(prefs.get_ignored_paths('report'))
    if not fmt or fmt == 'default':
        fmt = prefs.get('report.default_format')

    # use a list so we can iterate more than once
    characters = list(parser.get_characters(flatten(search), ignore))

    # Construct a dict keyed by tag name whose values are Counters. Each Counter
    # is initialized with a flattened list of lists and we let it count the
    # duplicates.
    table_data = {tag : Counter(flatten([c.tags.get(tag, 'None') for c in characters])) for tag in flatten(tags)}

    formatter = formatters.get_report_formatter(fmt)
    if not formatter:
        return result.OptionError(errmsg="Cannot create output of format '{}'".format(fmt))
    with util.smart_open(outfile, binary=(fmt in formatters.BINARY_TYPES)) as outstream:
        response = formatter(table_data, outstream=outstream, prefs=prefs)

    # pass errors straight through
    if not response.success:
        return response

    openable = [outfile] if outfile and outfile != '-' else None

    return result.Success(openable=openable)

def find(*rules, search=None, ignore=None, **kwargs):
    """
    Find characters in the campaign that match certain rules

    Searches for character objects in the campaign that match the given
    rules. To search an arbitrary list of Character objects, use
    find_characters.

    Args:
        rules (str): One or more strings that describe which characters to
            find. Passed directly to find_characters.
        search (list): Paths to search for character files. Items can be strings
            or lists of strings.
        ignore (list): Paths to ignore
        dryrun (bool): Whether to print the character file paths instead of
            opening them
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain a list of file paths to the
        matching Character objects.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    dryrun = kwargs.get('dryrun', False)
    if search is None:
        search = []

    if not ignore:
        ignore = []
    ignore.extend(prefs.get_ignored_paths('find'))

    rules = list(flatten(rules))

    # use a list so we can iterate more than once
    characters = list(parser.get_characters(flatten(search), ignore))

    filtered_chars = find_characters(rules, characters=characters)

    paths = [char.path for char in filtered_chars]

    if dryrun:
        openable = []
        printables = paths
    else:
        openable = paths
        printables = []

    return result.Success(openable=openable, printables=printables)

def find_characters(rules, characters):
    """
    Filter characters list according to the given rules

    Args:
        rules (list): One or more strings that describe which characters to
            find. Rules take the format `tag:text`. If `tag` is not given,
            `text` will be matched against each character's name. A character
            matches a rule when that character has at least one value for `tag`
            which matches or contains `text`. Multiple rules are tested
            sequentially from left to right. All tags and texts are
            case-insensitive.
        characters (list): List of Character objects to search

    Returns:
        List of character objects that match all of the rules.
    """

    rule = rules.pop(0)

    if "~:" in rule:
        sep = "~:"
        mod = lambda x: not x
    else:
        sep = ":"
        mod = lambda x: x

    parts = rule.split(sep, 1)

    if len(parts) == 2:
        tag = parts[0].strip().casefold()

        if not tag:
            # default to name tag
            tag = 'name'

        # expand abbreviations
        if tag == 'desc':
            tag = 'description'

        text = parts[1].strip().casefold()
    elif len(parts) == 1:
        tag = 'name'
        text = parts[0].strip().casefold()

    filtered_chars = [char for char in characters if mod(char.tags(tag).contains(text))]

    if not rules:
        return filtered_chars
    else:
        return find_characters(rules, filtered_chars)
