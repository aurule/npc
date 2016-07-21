"""
Markdown formatter for creating a page of characters.

Has a single entry point `dump`.
"""

from .. import util

def dump(characters, outstream, *, include_metadata=None, metadata=None):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        include_metadata (string|None): Whether to include metadata, and what
            format to use.What kind of metadata to include, if any. Accepts
            values of 'mmd', 'yaml', or 'yfm'. Metadata will always include a
            title and creation date.
        metadata (dict): Additional metadata to insert. Ignored unless
            include_metadata is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.

    Returns:
        A util.Result object. Openable will not be set.
    """
    if not metadata:
        metadata = {}

    if include_metadata:
        if include_metadata == 'mmd':
            metadata_lines = ['{}: {}'.format(k.title(), v) for k, v in metadata.items()]
            final_metadata = "  \n".join(metadata_lines)
        elif include_metadata in ('yaml', 'yfm'):
            metadata_lines = ['{}: {}'.format(k, v) for k, v in metadata.items()]
            final_metadata = "---\n" + "\n".join(metadata_lines) + "\n---\n"
        else:
            return util.Result(
                False,
                errmsg="Unrecognized metadata format option '{}'".format(include_metadata),
                errcode=6)

        outstream.write(final_metadata)

    for char in characters:
        # name (header)
        realname = char['name'][0]
        outstream.write("# {}".format(realname))
        if 'dead' in char:
            outstream.write(" (Deceased)")
        outstream.write("\n\n")

        # info block
        info_block = []
        _append_aka_line(char['name'], info_block)
        _append_titles_line(char.get('title', []), info_block)
        _append_character_type_line(char, info_block)
        _append_character_subtype_line(char, info_block)
        _append_secondary_groups(char, info_block)

        outstream.write('  \n'.join(info_block))
        outstream.write('\n')

        # show appearance descriptions
        appearance = _build_appearance(char)
        if appearance:
            outstream.write("\n")
            outstream.write(appearance)
            outstream.write("\n")

        # show description
        outstream.write("\n")
        outstream.write(char['description'])
        outstream.write("\n")

        # show description of death, if present
        if 'dead' in char and len(char['dead']) > 0:
            outstream.write("\n")
            outstream.write(' '.join(char['dead']))
            outstream.write("\n")

        outstream.write("\n")
    return util.Result(True)

def _get_character_type(char):
    return char['type'][0].lower()

def _append_aka_line(names, info_block):
    """
    Build the AKA line for a character's names

    Appends a line like "*AKA name1, name2*" to info_block.

    Args:
        names (list): Additional names for the character
        info_block (list): Target list of info lines
    """
    if len(names) > 1:
        info_block.append('*AKA {}*'.format(", ".join(names[1:])))

def _append_titles_line(titles, info_block):
    """
    Build the Titles line for a character's titles

    Appends a comma-spearated list of titles to info_block.

    Args:
        titles (list): Titles the character has
        info_block (list): Target list of info lines
    """
    if titles:
        info_block.append(', '.join(titles))

def _append_character_type_line(char, info_block):
    """
    Build the character type line

    Appends a line describing the character's type and primary affiliation to info_block.

    The values in this line vary by character type.

    * changeling:
        1. Changeling
        2. motley if present
        3. court if present
    * all others:
        1. character type name
        2. first @group if present

    Args:
        char (dict): Character information
        info_block (list): Target list of info lines
    """

    type_parts = []
    base = char['type'][0]
    if 'foreign' in char:
        base += ' in {}'.format(' and '.join(char['foreign']))
    type_parts.append(base)

    character_type_code = _get_character_type(char)
    if character_type_code == 'changeling':
        if 'motley' in char:
            motley = char['motley'][0]
            slug = _add_group_ranks('{} Motley'.format(motley, motley, char['rank']))
            type_parts.append(slug)

        if 'court' in char:
            court = char['court'][0]
            slug = _add_group_ranks('{} Court'.format(court, court, char['rank']))
            type_parts.append(slug)
    else:
        if 'group' in char:
            group = char['group'][0]
            slug = _add_group_ranks(group, group, char['rank'])
            type_parts.append(slug)

    info_block.append(', '.join(type_parts))

def _append_character_subtype_line(char, info_block):
    """
    Append the subtype line for a character

    Appends a line to info_block for certain character types.

    Changeling characters:
        1. Seemings, separated by a slash ('/')
        2. Kiths, separated by a slash ('/')
    All others:
        No subtype line is appended

    Args:
        char (dict): Character info
        info_block (list): Target list of info lines
    """
    character_type = _get_character_type(char)
    if character_type == 'changeling' and (
            'seeming' in char or
            'kith' in char):
        subtype_parts = []
        if 'seeming' in char:
            subtype_parts.append('/'.join(char['seeming']))
        if 'kith' in char:
            subtype_parts.append('/'.join(char['kith']))
        info_block.append(' '.join(subtype_parts))

def _add_group_ranks(slug, name, ranks):
    """
    Add ranks to a group

    Args:
        slug (str): Base group tag
        name (str): Raw group name
        char (dict): Character data

    Returns:
        Complete group string with ranks
    """
    if name in ranks:
        return slug + " ({})".format(', '.join(ranks[name]))

    return slug

def _append_secondary_groups(char, info_block):
    """
    Build lines for other groups the character belongs to

    The first group listed usually ends up in the character type line. This
    method builds the list of other groups. Its contents are somewhat dependent
    on the character's type.

    * changeling:
        1. Other courts (should never happen)
        2. Other motleys (should never happen)
        3. All @group entries
    * all others:
        1. All @motley entries
        2. All @group entries

    Args:
        char (dict): Character info
        info_block (list): Target list of info lines
    """
    group_parts = []

    character_type = _get_character_type(char)
    if character_type == "changeling":
        for court in char.get('court', [])[1:]:
            group_parts.append(_add_group_ranks('{} court'.format(court, court, char['rank'])))

    for motley in char.get('motley', [])[1:]:
        group_parts.append(_add_group_ranks('{} Motley'.format(motley, motley, char['rank'])))
    for group in char.get('group', []):
        group_parts.append(_add_group_ranks(group, group, char['rank']))

    if group_parts:
        info_block.append(', '.join(group_parts))

def _build_appearance(char):
    """
    Build the appearance description for the character

    The appearance is usually just the values of all @appearance tags. Some
    character types use their own special tags to extend or replace @appearance.

    * changeling:
        1. @appearance
        2. @mien
        3. @mask

    Args:
        char (dict): Character info

    Returns:
        Appearance description string
    """
    character_type = _get_character_type(char)
    if character_type == 'changeling':
        appearance_parts = []
        if 'appearance' in char:
            appearance_parts.append('*Appearance:* ' + ' '.join(char['appearance']))
        if 'mien' in char:
            appearance_parts.append('*Mien:* ' + ' '.join(char['mien']))
        if 'mask' in char:
            appearance_parts.append('*Mask:* ' + ' '.join(char['mask']))

        return "  \n".join(appearance_parts)
    else:
        if 'appearance' in char:
            return '*Appearance:* ' + ' '.join(char['appearance'])
