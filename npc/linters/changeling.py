import re

replaceable = ('x', 'y')
seeming_regex = '^(?P<name>\s+seeming\s+)(?P<seeming>%s)\s*(?P<notes>\(.*\))?$'
kith_regex = '^(?P<name>\s+kith\s+)(?P<kith>%s)\s*(?P<notes>\(.*\))?$'

def lint(c, fix = False, **kwargs):
    """Verify the more complex elements in a changeling sheet

    This method checks for changeling-specific problems within the rules blocks
    of the character sheet. The problems it checks for relate to the seeming and
    kith notes.

    1. Both elements must appear in the sheet's body -- not just the tags.
    2. Both elements must match the value of the corresponding tag.
    3. Both elements must have correct notes about its blessing (and curse for
        Seeming)

    Missing or incorrect notes can be fixed automatically if desired.

    The kwargs must contain:
    * sk: a parsed dict of blessings and curses, as from `support/seeming-kith.json`
    """
    problems = []
    dirty = False

    sk = kwargs['sk']

    # Check that seeming tag exists and is valid
    seeming_tags = None
    if not 'seeming' in c:
        problems.append("Missing @seeming tag")
    else:
        seeming_tags = [t.lower() for t in c['seeming']] # used later
        for seeming_name in c['seeming']:
            if seeming_name.lower() not in sk['blessing']:
                problems.append("Unrecognized @seeming '%s'" % seeming_name)

    # Check that kith tag exists and is valid
    kith_tags = None
    if not 'kith' in c:
        problems.append("Missing @kith tag")
    else:
        kith_tags = [t.lower() for t in c['kith']] # used later
        for kith_name in c['kith']:
            if kith_name.lower() not in sk['blessing']:
                problems.append("Unrecognized @kith '%s'" % kith_name)

    # tags are ok. now compare against listed seeming and kith in stats

    with open(c['path'], 'r') as f:
        data = f.read()

        if seeming_tags:
            # ensure the listed seemings match our seeming tags
            seeming_re = re.compile(
                seeming_regex % '\w+',
                re.MULTILINE | re.IGNORECASE
            )
            seeming_matches = list(seeming_re.finditer(data))
            seeming_stat_names = [m.group('seeming').lower() for m in seeming_matches]
            if set(seeming_tags) != set(seeming_stat_names):
                problems.append("Seeming stats do not match @seeming tags")
                if (len(seeming_stat_names) == 1
                    and len(seeming_tags) == 1
                    and seeming_stat_names[0] in replaceable):
                    if fix:
                        seeming_tag = seeming_tags[0]
                        try:
                            seeming_line = "%s (%s; %s)" % (seeming_tag.title(), sk['blessing'][seeming_tag], sk['curse'][seeming_tag])
                        except IndexError:
                            seeming_line = "%s" % seeming_tag.title()

                        data = seeming_re.sub(
                            '\g<1>%s' % seeming_line,
                            data
                        )
                        problems[-1] += ' (placeholder; FIXED)'
                        dirty = True
                    else:
                        problems[-1] += ' (placeholder; can fix)'
            else:
                # tags and stats match. iterate through each seeming and make sure the notes are right
                for m in list(seeming_matches):
                    seeming_tag = m.group('seeming').lower()
                    if not seeming_tag in sk['blessing']:
                        continue

                    loaded_seeming_notes = m.group('notes')
                    seeming_notes = "(%s; %s)" % (sk['blessing'][seeming_tag], sk['curse'][seeming_tag])
                    if not loaded_seeming_notes:
                        problems.append("Missing notes for Seeming '%s'" % m.group('seeming'))
                        if fix:
                            data = _fix_seeming_notes(m.group('seeming'), seeming_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'
                    else:
                        if loaded_seeming_notes != seeming_notes:
                            problems.append("Incorrect notes for Seeming '%s'" % m.group('seeming'))
                            if fix:
                                data = _fix_seeming_notes(m.group('seeming'), seeming_notes, data)
                                problems[-1] += ' (FIXED)'
                                dirty = True
                            else:
                                problems[-1] += ' (can fix)'


        if kith_tags:
            # ensure the listed kiths match our kith tags
            kith_re = re.compile(
                kith_regex % '\w+( \w+)?',
                re.MULTILINE | re.IGNORECASE
            )
            kith_matches = list(kith_re.finditer(data))
            kith_stat_names = [m.group('kith').lower() for m in kith_matches]
            if set(kith_tags) != set([m.group('kith').lower() for m in kith_matches]):
                problems.append("Kith stats do not match @kith tags")
                if (len(kith_stat_names) == 1
                    and len(kith_tags) == 1
                    and kith_stat_names[0] in replaceable):
                    if fix:
                        kith_tag = kith_tags[0]
                        try:
                            kith_line = "%s (%s)" % (kith_tag.title(), sk['blessing'][kith_tag])
                        except IndexError:
                            kith_line = "%s" % kith_tag.title()

                        data = kith_re.sub(
                            '\g<1>%s' % kith_line,
                            data
                        )
                        problems[-1] += ' (placeholder; FIXED)'
                        dirty = True
                    else:
                        problems[-1] += ' (placeholder; can fix)'
            else:
                # tags and stats match. iterate through each kith and make sure the notes are right
                for m in list(kith_matches):
                    kith_tag = m.group('kith').lower()
                    if not kith_tag in sk['blessing']:
                        continue

                    loaded_kith_notes = m.group('notes')
                    kith_notes = "(%s)" % (sk['blessing'][kith_tag])
                    if not loaded_kith_notes:
                        problems.append("Missing notes for Kith '%s'" % m.group('kith'))
                        if fix:
                            data = _fix_kith_notes(m.group('kith'), kith_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'
                    else:
                        if loaded_kith_notes != kith_notes:
                            problems.append("Incorrect notes for Kith '%s'" % m.group('kith'))
                            if fix:
                                data = _fix_kith_notes(m.group('kith'), kith_notes, data)
                                problems[-1] += ' (FIXED)'
                                dirty = True
                            else:
                                problems[-1] += ' (can fix)'

    if dirty and data:
        with open(c['path'], 'w') as f:
            f.write(data)

    return problems

def _fix_seeming_notes(seeming, notes, data):
    """Insert correct notes for a seeming stat"""
    seeming_fix_re = re.compile(
        seeming_regex % seeming,
        re.MULTILINE | re.IGNORECASE
    )
    return seeming_fix_re.sub(
        '\g<1>\g<2> %s' % notes,
        data
    )

def _fix_kith_notes(kith, notes, data):
    """Insert correct notes for a kith stat"""
    kith_fix_re = re.compile(
        kith_regex % kith,
        re.MULTILINE | re.IGNORECASE
    )
    return kith_fix_re.sub(
        '\g<1>\g<2> %s' % notes,
        data
    )
