#!/usr/bin/env python3.5

import re
import json
import sys
from contextlib import contextmanager
from datetime import datetime
from os import path, walk, makedirs, rmdir, scandir
from shutil import copy as shcopy, move as shmove
import itertools

# local packages
from . import formatters, linters, parser, util, settings

def create_changeling(args, prefs=settings.InternalSettings(), **kwargs):
    """Create a Changeling character.

    Arguments:
    * args - object containing runtime data. Must contain the following
             attributes:
        + name              string  Base file name
        + seeming           string  Name of the character's Seeming. Added to
                                    the file with notes.
        + kith              string  Name of the character's Kith. Added to the
                                    file with notes.
        + court (optional)  string  Name of the character's Court. Used to
                                    derive path.
        + motley (optional) string  Name of the character's Motley.
        + group (optional)  list    One or more names of groups the character
                                    belongs to. Used to derive path.
    * prefs - Settings object
    """
    seeming_re = re.compile(
        '^(\s+)seeming(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )
    kith_re = re.compile(
        '^(\s+)kith(\s+)\w+$',
        re.MULTILINE | re.IGNORECASE
    )

    # Derive the path for the new file
    target_path = _add_path_if_exists(prefs.get('paths.characters'), prefs.get('type_paths.%s' % 'changeling'))
    if args.court:
        target_path = _add_path_if_exists(target_path, args.court.title())
    else:
        target_path = _add_path_if_exists(target_path, 'Courtless')

    for group_name in args.groups:
        target_path = _add_path_if_exists(target_path, group_name)

    filename = args.name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % args.name, errcode = 1)

    # Create tags
    seeming_name = args.seeming.title()
    kith_name = args.kith.title()
    tags = ['@changeling %s %s' % (seeming_name, kith_name)]
    if args.motley:
        tags.append('@motley %s' % args.motley)
    if args.court:
        tags.append('@court %s' % args.court.title())
    tags.extend(_make_std_tags(groups = args.groups, dead = args.dead, foreign = args.foreign))

    header = "\n".join(tags) + '\n\n'

    # Copy template data
    try:
        with open(prefs.get('templates.changeling'), 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % prefs.get('templates.changeling'), errcode=4)

    # insert seeming and kith in the advantages block
    sk = prefs.get('changeling')
    seeming_key = args.seeming.lower()
    if seeming_key in sk['seemings']:
        seeming_notes = "%s; %s" % (sk['blessings'][seeming_key], sk['curses'][seeming_key])
        data = seeming_re.sub(
            '\g<1>Seeming\g<2>%s (%s)' % (seeming_name, seeming_notes),
            data
        )
    kith_key = args.kith.lower()
    if kith_key in sk['kiths']:
        kith_notes = sk['blessings'][kith_key]
        data = kith_re.sub(
            '\g<1>Kith\g<2>%s (%s)' % (kith_name, kith_notes),
            data
        )

    # Save the new character
    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def _make_std_tags(groups = [], dead = False, foreign = ""):
    """Create standard tags that apply to all character types.

    Arguments:
    groups -- Array of group names
    dead -- Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
    foreign -- Details of non-standard residence. Leave empty to exclude the
            @foreign tag.
    """
    tags = ["@group %s" % g for g in groups]
    if dead != False:
        dead_details = " %s" % dead if len(dead) else ""
        tags.append("@dead%s" % dead_details)
    if foreign:
        tags.append("@foreign %s" % foreign)
    return tags

def create_simple(name, ctype, groups=[], dead=False, foreign=False, prefs=settings.InternalSettings(), **kwargs):
    """Create a character without extra processing.

    Simple characters don't have any unique tags or file annotations. Everything
    is based on their type.

    Arguments:
    + name              string  Base file name
    * ctype string  Character type
    + group (optional)  list    One or more names of groups the character
                                belongs to. Used to derive path for the file.
    dead -- Whether to add the @dead tag. Pass False to exclude it
            (the default), an empty string to inlcude it with no details given,
            and a non-empty string to include the tag along with the contents of
            the argument.
    foreign -- Details of non-standard residence. Leave empty to exclude the
            @foreign tag.
    """
    if ctype not in prefs.get('templates'):
        return Result(False, errmsg="Unrecognized template '%s'" % ctype, errcode=7)

    # Derive destination path
    target_path = _add_path_if_exists(prefs.get('paths.characters'), prefs.get('type_paths.%s' % ctype))
    for group_name in groups:
        target_path = _add_path_if_exists(target_path, group_name)

    filename = name + '.nwod'
    target_path = path.join(target_path, filename)
    if path.exists(target_path):
        return Result(False, errmsg="Character '%s' already exists!" % name, errcode = 1)

    # Add tags
    typetag = ctype.title()
    tags = ['@type %s' % typetag] + _make_std_tags(groups = groups, dead = dead, foreign = foreign)
    header = "\n".join(tags) + '\n\n'

    # Copy template
    template = prefs.get('templates.%s' % ctype)
    try:
        with open(template, 'r') as f:
            data = header + f.read()
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % template, errcode=4)

    # Write the new file
    try:
        with open(target_path, 'w') as f:
            f.write(data)
    except IOError as e:
        return Result(False, errmsg=e.strerror + " (%s)" % target_path, errcode=4)

    return Result(True, openable = [target_path])

def _add_path_if_exists(base, potential):
    """Add a directory to the base path if that directory exists."""
    test_path = path.join(base, potential)
    if path.exists(test_path):
        return test_path
    return base

def session(prefs=settings.InternalSettings(), **kwargs):
    """Creates the files for a new game session.

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log.
    """
    plot_re = re.compile('(?i)^plot (\d+)$')
    session_re = re.compile('(?i)^session (\d+)$')

    # find latest plot file and its number
    plot_files = [f.name for f in scandir(prefs.get('paths.plot')) if f.is_file() and plot_re.match(path.splitext(f.name)[0])]
    try:
        latest_plot = max(plot_files, key=lambda plot_files:re.split(r"\s", plot_files)[1])
        (latest_plot_name, latest_plot_ext) = path.splitext(latest_plot)
        plot_match = plot_re.match(latest_plot_name)
        plot_number = int(plot_match.group(1))
    except ValueError:
        plot_number = 0

    # find latest session log and its number
    session_files = [f.name for f in scandir(prefs.get('paths.session')) if f.is_file() and session_re.match(path.splitext(f.name)[0])]
    try:
        latest_session = max(session_files, key=lambda session_files:re.split(r"\s", session_files)[1])
        (latest_session_name, latest_session_ext) = path.splitext(latest_session)
        session_match = session_re.match(latest_session_name)
        session_number = int(session_match.group(1))
    except ValueError:
        session_number = 0

    new_number = min(plot_number, session_number) + 1

    openable = []
    if session_number:
        if session_number < new_number:
            # create new session log
            old_session_path = path.join(prefs.get('paths.session'), latest_session)
            new_session_path = path.join(prefs.get('paths.session'), ("session %i" % new_number) + latest_session_ext)
            shcopy(prefs.get('templates.session'), new_session_path)
        else:
            # present existing plot files, since we don't have to create one
            old_session_path = path.join(prefs.get('paths.session'), ("session %i" % (session_number - 1)) + latest_session_ext)
            new_session_path = path.join(prefs.get('paths.session'), latest_session)
        openable.extend( (new_session_path, old_session_path) )
    else:
        # no old session
        new_session_path = path.join(prefs.get('paths.session'), ("session %i.md" % new_number))
        shcopy(prefs.get('templates.session'), new_session_path)
        openable.append(new_session_path)

    if plot_number:
        if plot_number < new_number:
            # copy old plot
            old_plot_path = path.join(prefs.get('paths.plot'), latest_plot)
            new_plot_path = path.join(prefs.get('paths.plot'), ("plot %i" % new_number) + latest_plot_ext)
            shcopy(old_plot_path, new_plot_path)
        else:
            # present existing sessions files, since we don't have to create one
            old_plot_path = path.join(prefs.get('paths.plot'), ("plot %i" % (plot_number - 1)) + latest_plot_ext)
            new_plot_path = path.join(prefs.get('paths.plot'), latest_plot)
        openable.extend( (new_plot_path, old_plot_path) )
    else:
        # no old plot to copy, so use a blank
        new_plot_path = path.join(prefs.get('paths.plot'), ("plot %i.md" % new_number))
        with open(new_plot_path, 'w') as f:
            f.write(' ')
        openable.append(new_plot_path)

    return Result(True, openable=openable)

def reorg(search, ignore=[], purge=False, verbose=False, prefs=settings.InternalSettings(), **kwargs):
    """Move character files into the correct paths.

    Character files are moved so that their path matches the ideal path as
    closely as possible. No new directories are created.

    Arguments:
    * search    array   Array of paths to search for character files
    * ignore    array   Array of paths to ignore
    * purge     bool    Flag indicating that empty directories should be
                        deleted after all files have been moved.
    * verbose   bool    Whether to print changes as they are made
    * prefs - settings object
    """
    base_path = prefs.get('paths.characters')
    characters = parser.get_characters(search, ignore)
    for c in characters:
        new_path = create_path_from_character(c, base_path, prefs)
        if new_path != path.dirname(c['path']):
            if verbose:
                print("Moving {} to {}".format(c['path'], new_path))
            shmove(c['path'], new_path)

    if purge:
        for empty_path in find_empty_dirs(base_path):
            rmdir(empty_path)
            if verbose:
                print("Removing empty directory {}".format(empty_path))

    return Result(True)

def find_empty_dirs(root):
    """Find empty directories under root"""
    for dirpath, dirs, files in walk(root):
        if not dirs and not files:
            yield dirpath

def create_path_from_character(character, target_path, prefs=settings.InternalSettings()):
    """Determine the best file path for a character.

    The path is created underneath target_path. It only includes directories
    which already exist.

    Arguments:
    * character -- dict containing parsed character data
    * target_path -- base path
    * prefs -- settings object
    """
    # add type-based directory if we can
    if 'type' in character:
        ctype = character['type'][0].lower()
        target_path = _add_path_if_exists(target_path, prefs.get('type_paths.%s' % ctype))
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

    # everyone uses groups in their path
    if 'group' in character:
        for group_name in character['group']:
            target_path = _add_path_if_exists(target_path, group_name)

    return target_path

def list(args, prefs=settings.InternalSettings(), **kwargs):
    """Generate a list of NPCs.

    Arguments:
    * args - object containing runtime data. Must contain the following:
        + search    array       Array of paths to search for character files
        + ignore    array       Array of paths to ignore
        + format    string      Format of the output. Supported types are
                                markdown (md), and json.
        + metadata  None|string Optional flag to include metadata in the output.
                                Additionally, the metadata format can be
                                specified for some output formats. The markdown
                                format supports adding either mmd
                                (MultiMarkdown) or yfm/yaml (Yaml Front Matter)
                                metadata.
        + outfile   string      Optional path to a file to hold the generated
                                listing. If omitted, the data will be printed to
                                stdout.
    * prefs - Settings object
    """
    characters = _sort_chars(_prune_chars(parser.get_characters(args.search, args.ignore)))

    out_type = args.format.lower()

    if out_type in ('md', 'markdown'):
        # ensure 'default' gets replaced with the right default metadata format
        metadata_type = args.metadata
        if metadata_type == 'default':
            metadata_type = prefs.get('metadata_format.markdown')

        # call out to get the markdown
        with _smart_open(args.outfile) as f:
            meta = prefs.get_metadata('markdown')
            response = formatters.markdown.dump(characters, f, metadata_type, meta)
    elif out_type == 'json':
        # make some json
        meta = None
        if args.metadata:
            base_meta = {
                'meta': True,
                'title': 'NPC Listing',
                'created': datetime.now().isoformat()
            }
            meta = {**base_meta, **prefs.get_metadata('json')}

        with _smart_open(args.outfile) as f:
            response = formatters.json.dump(characters, f, meta)

    else:
        return Result(False, errmsg="Cannot create output of format '%s'", errcode=5)

    if not response.success:
        return response

    openable = None
    if args.outfile and args.outfile != '-':
        openable = [args.outfile]

    return Result(True, openable=openable)

def _sort_chars(characters):
    """Sort a list of character dicts.

    In the future, this is where different sort methods will be handled. Right
    now, it just sorts them by their "last" name (space-delimeted).

    Arguments:
    characters -- list of character dicts
    """
    return sorted(characters, key=lambda c: c['name'][0].split(' ')[-1])

def _prune_chars(characters):
    """Alter character records for output.

    This applies behavior from directives and certain tags. Specifically, it
    handles skip, it overrides type with faketype, and it inserts a placeholder
    type if one was not specified.

    Arguments:
    characters -- list of character dicts
    """

    for c in characters:
        # skip if asked
        if 'skip' in c:
            continue

        # use fake types if present
        if 'faketype' in c:
            c['type'] = c['faketype']

        # Use a placeholder for unknown type
        if 'type' not in c:
            c['type'] = 'Unknown'

        yield c

@contextmanager
def _smart_open(filename=None):
    """Open a named file or stdout as appropriate

    When filename is None or the dash character ('-'), this method will yield
    sys.stdout. When filename is a path, it will open the file for writing.
    Either way, a file-like object is returned.

    This method is designed to be used in a `with` block.
    """
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def dump(search, ignore=[], sort=False, metadata=False, outfile=None, prefs=settings.InternalSettings(), **kwargs):
    """Dump the raw character data, unaltered.

    Always formats the data as json.

    Arguments:
    * search    array       Array of paths to search for character files
    * ignore    array       Array of paths to ignore
    * sort      bool        Whether to sort the characters before dumping
    * metadata  bool        Whether to prepend metadata to the output
    * outfile   None|string Filename to put the dumped data. None and "-" print
    *     to stdout.
    """
    characters = parser.get_characters(search, ignore)
    if sort:
        characters = _sort_chars(characters)

    # make some json
    if metadata:
        base_meta = {
            'meta': True,
            'title': 'NPC Listing',
            'created': datetime.now().isoformat()
        }
        meta = {**base_meta, **prefs.get_metadata('json')}
        characters = itertools.chain([meta], characters)

    with _smart_open(outfile) as f:
        json.dump([c for c in characters], f)

    openable = None
    if outfile and outfile != '-':
        openable = [outfile]

    return Result(True, openable=openable)

def lint(search, ignore=[], fix=False, prefs=settings.InternalSettings(), **kwargs):
    """Check character files for completeness and correctness

    Arguments:
    + search    array   Array of paths to search for character files
    + ignore    array   Array of paths to ignore
    + fix       boolean Whether to automatically fix errors when possible
    * prefs object  Settings object

    This method checks that every character file has a few required tags, and
    applies extra checking for some character types.

    Required tags:
    * description - Not a tag, but the file must have description content
    * @type - Character type

    Extra checks for Changelings:
    * @seeming tag is present and valid
    * @kith tag is present and valid
    """

    openable = []
    problems = []

    # check each character
    characters = parser.get_characters(search, ignore)
    for c in characters:
        # Check description
        if not c['description'].strip():
            problems.append("Missing description")

        # Check type tag
        if not 'type' in c:
            problems.append("Missing @type tag")
        else:
            # Do additional processing based on reported type
            types = [t.lower() for t in c['type']]
            if 'changeling' in types:
                # find (and fix) changeling-specific problems in the body of the sheet
                problems.extend(linters.changeling.lint(c, fix, sk=prefs.get('changeling')))

        # Report problems on one line if possible, or as a block if there's more than one
        if len(problems):
            openable.append(c['path'])
            if len(problems) > 1:
                print("File '%s':" % c['path'])
                for p in problems:
                    print("    %s" % p)
            else:
                print("%s in '%s'" % (problems[0], c['path']))

    return Result(True, openable)

def init(create_types = False, create_all = False, prefs=settings.InternalSettings(), **kwargs):
    """Create the basic directories for a campaign

    This will create the directories this tool expects to find within a
    campaign. Other directories are left to the user.

    Arguments:
    create_types -- Whether to create directories for each character type
    create_all -- Whether to create all optional directories. Overrides `types`.
    """
    for k, p in prefs.get('paths').items():
        makedirs(p, mode=0o775, exist_ok=True)
    makedirs('.npc', mode=0o775, exist_ok=True)

    if create_types or create_all:
        cbase = prefs.get('paths.characters')
        for k, p in prefs.get('type_paths').items():
            makedirs(path.join(cbase, p), mode=0o775, exist_ok=True)

    return Result(True)

def settings(location, show_defaults = False, prefs=settings.InternalSettings(), **kwargs):
    """Open the named settings file

    If the desired settings file does not exist, an empty file is created and
    then opened.

    Arguments:
    location -- Which settings file to open. One of 'user' or 'campaign'.
    show_defaults -- Whether the default settings file should be opened for
        reference alongside the specified settings file.
    """
    target_path = prefs.get_settings_path(location)
    if not path.exists(target_path):
        dirname = path.dirname(target_path)
        makedirs(dirname, mode=0o775, exist_ok=True)
        open(target_path, 'a').close()

    if show_defaults:
        openable = [prefs.get_settings_path('default'), target_path]
    else:
        openable = [target_path]
    return Result(True, openable = openable)

class Result:
    """Data about the result of a subcommand

    Attributes:
    * success   boolean Whether the subcommand ran correctly
    * openable  list    Paths to files which were changed by or are relevant to
                        the subcommand
    * errcode   integer Error code indicating the type of error encountered
    * errmsg    string  Human-readable error message. Will be displayed to the
                        user
    """
    def __init__(self, success, openable = None, errcode = 0, errmsg = ''):
        super(Result, self).__init__()
        self.success = success
        self.openable = openable
        self.errcode = errcode
        # Error codes:
        # 0. Everything's fine
        # 1. Tried to create a file that already exists
        # 2. Latest plot and session files have different numbers
        # 3. Feature is not yet implemented
        # 4. Filesystem error
        # 5. Unrecognized format
        # 6. Invalid option
        # 7. Unrecognized template
        # 8. Missing required file
        self.errmsg = errmsg
