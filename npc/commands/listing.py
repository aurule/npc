"""
Module for creating a list of characters
"""

from npc import settings, parser, formatters
from npc.util import flatten, result

from . import util

def make_list(*search, ignore=None, fmt=None, metadata=None, title=None, outfile=None, **kwargs):
    """
    Generate a listing of NPCs.

    The default listing templates ignore tags not found in Character.KNOWN_TAGS.

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
        do_sort (bool): Whether to avoid sorting altogether. Defaults to True.
        sort_by (string|None): Sort order for characters. Defaults to the value of
            "list_sort" in settings.
        group_by (List[string]): List of tag names to group characters by
        prefs (Settings): Settings object to use. Uses internal settings by
            default.
        progress (function): Callback function to track the progress of
            generating a listing. Must accept the current count and total count.
            Should print to stderr. Not used by all formatters.

    Returns:
        Result object. Openable will contain the output file if given.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not ignore:
        ignore = []
    ignore.extend(prefs.get_ignored_paths('listing'))
    sort_order = kwargs.get('sort_by', prefs.get('listing.sort_by'))
    do_sort = kwargs.get('do_sort', True)
    group_by = kwargs.get('group_by', [])
    update_progress = kwargs.get('progress', lambda i, t: False)

    characters = _process_directives(parser.get_characters(flatten(search), ignore))
    if do_sort:
        sorter = util.character_sorter.CharacterSorter(sort_order, prefs=prefs)
        characters = sorter.sort(characters)

    if fmt == "default" or not fmt:
        fmt = prefs.get('listing.default_format')
    out_type = formatters.get_canonical_format_name(fmt)

    formatter = formatters.get_listing_formatter(out_type)
    if not formatter:
        return result.OptionError(errmsg="Cannot create output of format '{}'".format(out_type))

    if metadata == 'default' and out_type != 'json':
        # Ensure 'default' metadata type gets replaced with the right default
        # metadata format. Irrelevant for json format.
        metadata_type = prefs.get('listing.metadata.{}.default_format'.format(out_type))
    else:
        metadata_type = metadata

    meta = prefs.get_metadata(out_type)
    if title:
        meta['title'] = title

    sectioners = [formatters.sectioners.get_sectioner(tag=g, heading_level=i+1, prefs=prefs) for i, g in enumerate(group_by)]

    with util.smart_open(outfile, binary=(out_type in formatters.BINARY_TYPES)) as outstream:
        response = formatter(
            characters,
            outstream,
            include_metadata=metadata_type,
            metadata=meta,
            prefs=prefs,
            sectioners=sectioners,
            progress=update_progress)

    # pass errors straight through
    if not response.success:
        return response

    openable = [outfile] if outfile and outfile != '-' else None

    return result.Success(openable=openable)

def _process_directives(characters):
    """
    Alter character records for output.

    Warning: This function will modify the objects in `characters`.

    Applies behavior from directives:

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
