from datetime import datetime
from .. import commands

def dump(characters, f, metadata_type=None, metadata_extra={}):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        f (stream): Output stream
        metadata_type (string|None): What kind of metadata to include, if any.
            Accepts values of 'mmd', 'yaml', or 'yfm'. Metadata will always
            include a title and creation date.
        metadata_extra (dict): Additional metadata keys to insert. Ignored
            unless metadata_type is set.

    Returns:
        A commands.Result object. Openable will not be set.
    """
    if metadata_type:
        if metadata_type in 'mmd':
            metadata_extra = ['{}: {}  '.format(k, v) for k, v in metadata_extra.items()]

            meta = [
                'Title: NPC Listing  ',
                'Created: %s  ' % datetime.now().isoformat()
            ] + metadata_extra + ['\n']
        elif metadata_type in ('yaml', 'yfm'):
            metadata_extra = ['{}: {}'.format(k, v) for k, v in metadata_extra.items()]

            meta = [
                '---',
                'title: NPC Listing',
                'created: %s' % datetime.now().isoformat()
            ] + metadata_extra + ['---\n']
        else:
            return commands.Result(False, errmsg="Unrecognized metadata format option '%s'" % metadata_type, errcode=6)
        data = "\n".join(meta)
        f.write(data)

    for c in characters:
        # name (header)
        realname = c['name'][0]
        f.write("# %s" % realname)
        if 'dead' in c:
            f.write(" (Deceased)")
        f.write("\n\n")

        # info block
        info_block = []

        # AKA line (info block)
        if len(c['name']) > 1:
            info_block.append('*AKA %s*' % "; ".join(c['name'][1:]))

        # character type and dependent values (info block)
        info_block.append(_build_character_type(c))

        # subtype information (info block)
        subtype = _build_character_subtype(c)
        if subtype:
            info_block.append(subtype)

        # list all groups (info block)
        secondary_groups = _build_secondary_groups(c)
        if secondary_groups:
            info_block.append('Member of %s' % secondary_groups)

        f.write('  \n'.join(info_block))
        f.write('\n')

        # show appearance descriptions
        appearance = _build_appearance(c)
        if appearance:
            f.write("\n")
            f.write(appearance)
            f.write("\n")

        # show description
        f.write("\n")
        f.write(c['description'])
        f.write("\n")

        # show description of death, if present
        if 'dead' in c and len(c['dead']) > 0:
            f.write("\n")
            f.write(' '.join(c['dead']))
            f.write("\n")

        f.write("\n")
    return commands.Result(True)

def _build_character_type(c):
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
        c (dict): Character data

    Returns:
        String of character type info
    """
    character_type = c['type'][0].lower()
    if character_type == 'changeling':
        s = []
        base = 'Changeling'
        if 'foreign' in c:
            base += ' in %s' % ' and '.join(c['foreign'])
        s.append(base)
        if 'motley' in c:
            motley = c['motley'][0]
            slug = _add_group_ranks('%s Motley' % motley, motley, c)
            s.append(slug)

        if 'court' in c:
            court = c['court'][0]
            slug = _add_group_ranks('%s Court' % court, court, c)
            s.append(slug)

        return ', '.join(s)
    else:
        s = []
        base = c['type'][0]
        if 'foreign' in c:
            base += ' in %s' % ' and '.join(c['foreign'])
        s.append(base)
        if 'group' in c:
            group = c['group'][0]
            slug = _add_group_ranks(group, group, c)
            s.append(slug)

        return ', '.join(s)

def _add_group_ranks(slug, name, c):
    """
    Add ranks to a group

    Args:
        slug (str): Base group tag
        name (str): Raw group name
        c (dict): Character data

    Returns:
        Complete group string with ranks
    """
    if name in c['rank']:
        slug += " (%s)" % ', '.join(c['rank'][name])
    return slug

def _build_character_subtype(c):
    """
    Build the subtype string for a character

    The subtype may or may not exist based on the character's type. It also
    takes different forms based on type.

    * changeling:
        1. Seemings, separated by a slash ('/')
        2. Kiths, separated by a slash ('/')
    * all others: no subtype (returns None)

    Args:
        c (dict): Character info

    Returns:
        String of character subtype information, or None if no subtype info is present/matters
    """
    character_type = c['type'][0].lower()
    if character_type == 'changeling' and (
        'seeming' in c or
        'kith' in c):
        s = []
        if 'seeming' in c:
            s.append('/'.join(c['seeming']))
        if 'kith' in c:
            s.append('/'.join(c['kith']))
        return ' '.join(s)
    else:
        return None

def _build_secondary_groups(c):
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
        c (dict): Character info

    Returns:
        Description of the groups the character belongs to
    """
    character_type = c['type'][0].lower()
    if character_type == "changeling":
        s = []
        if 'court' in c and len(c['court']) > 1:
            for court in c['court'][1:]:
                slug = _add_group_ranks('%s court' % Court, court, c)
                s.append(slug)
        if 'motley' in c and len(c['motley']) > 1:
            for motley in c['motley'][1:]:
                slug = _add_group_ranks('%s Motley' % motley, motley, c)
                s.append(slug)
        if 'group' in c:
            for group in c['group']:
                slug = _add_group_ranks(group, group, c)
                s.append(slug)

        return ', '.join(s)
    else:
        s = []
        if 'motley' in c and len(c['motley']) > 1:
            for motley in c['motley'][1:]:
                slug = _add_group_ranks('%s Motley' % motley, motley, c)
                s.append(slug)
        if 'group' in c:
            for group in c['group'][1:]:
                slug = _add_group_ranks(group, group, c)
                s.append(slug)

        return ', '.join(s)

def _build_appearance(c):
    """
    Build the appearance description for the character

    The appearance is usually just the values of all @appearance tags. Some
    character types use their own special tags to extend or replace @appearance.

    * changeling:
        1. @appearance
        2. @mien
        3. @mask

    Args:
        c (dict): Character info

    Returns:
        Appearance description string
    """
    character_type = c['type'][0].lower()
    if character_type == 'changeling':
        s = []
        if 'appearance' in c:
            s.append('*Appearance:* ' + ' '.join(c['appearance']))
        if 'mien' in c:
            s.append('*Mien:* ' + ' '.join(c['mien']))
        if 'mask' in c:
            s.append('*Mask:* ' + ' '.join(c['mask']))

        return "  \n".join(s)
    else:
        if 'appearance' in c:
            return '*Appearance:* ' + ' '.join(c['appearance'])
