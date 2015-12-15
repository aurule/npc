from datetime import datetime

def dump(characters, f, metadata_type=None, metadata_extra={}):
    # make some markdown
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
            return Result(False, errmsg="Unrecognized metadata format option '%s'" % metadata_type, errcode=6)
        data = "\n".join(meta)
        f.write(data)

    for c in characters:
        # name
        realname = c['name'][0]
        f.write("# %s" % realname)
        if 'dead' in c:
            f.write(" (Deceased)")
        f.write("\n\n")

        # AKA line
        if len(c['name']) > 1:
            f.write("*AKA ")
            f.write(", ".join(c['name'][1:]))
            f.write("*\n")

        # character type and dependent values
        f.write(_build_character_type(c))
        f.write("\n")

        # subtype information
        subtype = _build_character_subtype(c)
        if subtype:
            f.write(subtype)
            f.write("\n")

        # list all groups
        secondary_groups = _build_secondary_groups(c)
        if secondary_groups:
            f.write("Member of ")
            f.write(secondary_groups)
            f.write("\n")

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

def _build_character_type(c):
    """Build the character type line

    The values in this line vary by character type.

    * changeling:
        1. Changeling
        2. motley if present
        3. court if present
    * all others:
        1. character type name
        2. first @group if present
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
    """Add ranks to a group"""
    if name in c['rank']:
        slug += " (%s)" % ', '.join(c['rank'][name])
    return slug

def _build_character_subtype(c):
    """Build the subtype string for a character

    The subtype may or may not exist based on the character's type. It also
    takes different forms based on type.

    * changeling:
        1. Seemings, separated by a slash ('/')
        2. Kiths, separated by a slash ('/')
    * all others: no subtype (returns None)
    """
    character_type = c['type'][0].lower()
    if character_type == 'changeling':
        s = []
        if 'seeming' in c:
            s.append('/'.join(c['seeming']))
        if 'kith' in c:
            s.append('/'.join(c['kith']))
        return ' '.join(s)
    else:
        return None

def _build_secondary_groups(c):
    """Build the list of other groups the character belongs to

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
    """
    character_type = c['type'][0].lower()
    if character_type == "changeling":
        s = []
        if 'court' in c and len(c['court']) > 1:
            for court in c['court'][1:0]:
                slug = _add_group_ranks('%s court' % Court, court, c)
                s.append(slug)
        if 'motley' in c and len(c['motley']) > 1:
            for motley in c['motley'][1:0]:
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
            for motley in c['motley'][1:0]:
                slug = _add_group_ranks('%s Motley' % motley, motley, c)
                s.append(slug)
        if 'group' in c:
            for group in c['group']:
                slug = _add_group_ranks(group, group, c)
                s.append(slug)

        return ', '.join(s)

def _build_appearance(c):
    """Build the appearance description for the character

    The appearance is usually just the values of all @appearance tags. Some
    character types use their own special tags to extend or replace @appearance.

    * changeling:
        1. @appearance
        2. @mien
        3. @mask
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

        return "\n".join(s)
    else:
        if 'appearance' in c:
            return '*Appearance:* ' + ' '.join(c['appearance'])
