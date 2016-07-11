"""
Markdown formatter for creating a page of characters.

Has a single entry point `dump`.
"""

from datetime import datetime
from .. import commands

def dump(characters, outstream, *, include_metadata=None, metadata_extra=None):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        include_metadata (string|None): Whether to include metadata, and what
            format to use.What kind of metadata to include, if any. Accepts
            values of 'mmd', 'yaml', or 'yfm'. Metadata will always include a
            title and creation date.
        metadata_extra (dict): Additional metadata to insert. Ignored unless
            include_metadata is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.

    Returns:
        A commands.Result object. Openable will not be set.
    """
    if not metadata_extra:
        metadata_extra = {}

    if include_metadata:
        default_metadata = {
            'title': 'NPC Listing',
            'created': datetime.now().isoformat()
        }
        metadata_raw = {**default_metadata, **metadata_extra}
        if include_metadata in 'mmd':
            metadata_lines = ['{}: {}'.format(k.title(), v) for k, v in metadata_raw.items()]
            metadata = "  \n".join(metadata_lines)
        elif include_metadata in ('yaml', 'yfm'):
            metadata_lines = ['{}: {}'.format(k, v) for k, v in metadata_raw.items()]
            metadata = "---\n" + "\n".join(metadata_lines) + "\n---\n"
        else:
            return commands.Result(
                False,
                errmsg="Unrecognized metadata format option '%s'" % include_metadata,
                errcode=6)

        outstream.write(metadata)

    for char in characters:
        # name (header)
        realname = char['name'][0]
        outstream.write("# %s" % realname)
        if 'dead' in char:
            outstream.write(" (Deceased)")
        outstream.write("\n\n")

        # info block
        info_block = []

        # AKA line (info block)
        if len(char['name']) > 1:
            info_block.append('*AKA %s*' % ", ".join(char['name'][1:]))

        #  Titles line (info block)
        if 'title' in char:
            info_block.append(', '.join(char['title']))

        # character type and dependent values (info block)
        info_block.append(_build_character_type(char))

        # subtype information (info block)
        subtype = _build_character_subtype(char)
        if subtype:
            info_block.append(subtype)

        # list all groups (info block)
        secondary_groups = _build_secondary_groups(char)
        if secondary_groups:
            info_block.append('Member of %s' % secondary_groups)

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
    return commands.Result(True)

def _build_character_type(char):
    """
    Build the character type line

    The values in this line vary by character type.

    * changeling:
        1. Changeling
        2. motley if present
        3. court if present
    * all others:
        1. character type name
        2. first @group if present

    Args:
        char (dict): Character data

    Returns:
        String of character type info
    """
    character_type = char['type'][0].lower()
    if character_type == 'changeling':
        type_parts = []
        base = 'Changeling'
        if 'foreign' in char:
            base += ' in %s' % ' and '.join(char['foreign'])
        type_parts.append(base)
        if 'motley' in char:
            motley = char['motley'][0]
            slug = _add_group_ranks('%s Motley' % motley, motley, char)
            type_parts.append(slug)

        if 'court' in char:
            court = char['court'][0]
            slug = _add_group_ranks('%s Court' % court, court, char)
            type_parts.append(slug)

        return ', '.join(type_parts)
    else:
        type_parts = []
        base = char['type'][0]
        if 'foreign' in char:
            base += ' in %s' % ' and '.join(char['foreign'])
        type_parts.append(base)
        if 'group' in char:
            group = char['group'][0]
            slug = _add_group_ranks(group, group, char)
            type_parts.append(slug)

        return ', '.join(type_parts)

def _add_group_ranks(slug, name, char):
    """
    Add ranks to a group

    Args:
        slug (str): Base group tag
        name (str): Raw group name
        char (dict): Character data

    Returns:
        Complete group string with ranks
    """
    if name in char['rank']:
        slug += " (%s)" % ', '.join(char['rank'][name])
    return slug

def _build_character_subtype(char):
    """
    Build the subtype string for a character

    The subtype may or may not exist based on the character's type. It also
    takes different forms based on type.

    * changeling:
        1. Seemings, separated by a slash ('/')
        2. Kiths, separated by a slash ('/')
    * all others: no subtype (returns None)

    Args:
        char (dict): Character info

    Returns:
        String of character subtype information, or None if no subtype info is present/matters
    """
    character_type = char['type'][0].lower()
    if character_type == 'changeling' and (
            'seeming' in char or
            'kith' in char):
        subtype_parts = []
        if 'seeming' in char:
            subtype_parts.append('/'.join(char['seeming']))
        if 'kith' in char:
            subtype_parts.append('/'.join(char['kith']))
        return ' '.join(subtype_parts)
    else:
        return None

def _build_secondary_groups(char):
    """
    Build the list of other groups the character belongs to

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

    Returns:
        Description of the groups the character belongs to
    """
    character_type = char['type'][0].lower()
    group_parts = []
    if character_type == "changeling":
        if 'court' in char and len(char['court']) > 1:
            for court in char['court'][1:]:
                slug = _add_group_ranks('%s court' % court, court, char)
                group_parts.append(slug)
        if 'motley' in char and len(char['motley']) > 1:
            for motley in char['motley'][1:]:
                slug = _add_group_ranks('%s Motley' % motley, motley, char)
                group_parts.append(slug)
        if 'group' in char:
            for group in char['group']:
                slug = _add_group_ranks(group, group, char)
                group_parts.append(slug)

        return ', '.join(group_parts)
    else:
        if 'motley' in char and len(char['motley']) > 1:
            for motley in char['motley'][1:]:
                slug = _add_group_ranks('%s Motley' % motley, motley, char)
                group_parts.append(slug)
        if 'group' in char:
            for group in char['group'][1:]:
                slug = _add_group_ranks(group, group, char)
                group_parts.append(slug)

        return ', '.join(group_parts)

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
    character_type = char['type'][0].lower()
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
