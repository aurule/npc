"""
Linter for verifying changeling files

Checks for a number of problems that are specific to changeling characters. The
only public entry point is the lint function.
"""

import re
from . import nwod
import npc
from npc.util import flatten

REPLACEABLE = ('x', 'y')
"""Standard placeholder values for seeming and kith"""

SEEMING_REGEX = r'^(?P<name>\s+seeming\s+)(?P<seeming>{})[ \t]*(?P<notes>\(.*\))?$'
"""Regex to match a seeming line"""

KITH_REGEX = r'^(?P<name>\s+kith\s+)(?P<kith>{})[ \t]*(?P<notes>\(.*\))?$'
"""Regex to match a kith line"""

STANDARD_MANTLE_REGEX = r'^\s+mantle\s+\((?P<court>[a-zA-Z ]+)\)'
"""Regex to match the standard way of writing the mantle merit: Mantle (court)."""

ALT_MANTLE_REGEX = r'^\s+(?P<court>[a-zA-Z]+) (?:court )?mantle'
"""
Regex to match alternate ways of writing the mantle merit: `court Court Mantle`,
or `court Mantle`.
"""

STANDARD_GOODWILL_REGEX = r'^\s+(?:court )?goodwill\s+\((?P<court>[a-zA-Z ]+)\)'
"""
Regex to match the standard way of writing the mantle merit: Goodwill (court).
"""

ALT_GOODWILL_REGEX = r'^\s+(?P<court>[a-zA-Z]+) (?:court )?goodwill'
"""
Regex to match alternate ways of writing the goodwill merit:
`court Court Goodwill`, or `court Goodwill`.
"""

UNSEEN_SENSE_REGEX = r'^\s+Unseen Sense\s+\((?P<thing>[\w\s]+)\)'

def lint(character, fix=False, *, strict=False, sk_data=None):
    """
    Verify the more complex elements in a changeling sheet.

    Checks for changeling-specific problems within the rules blocks of the
    character sheet. The problems it checks for are as follows:

    1. Seeming and kith appear in sk_data
    2. Entitlement tag appears at most one time
    2. Mantle merit matches court tag and appears at most one time
    3. Court Goodwill merit must not match mantle or court tag
    4. Seeming and kith appear in the sheet's body, not just the tags.
    5. Seeming and kith match the value of their corresponding tag.
    6. Seeming and kith have correct notes for their blessing (and curse for
        Seeming)

    Additional checks when strict is true:

    1. Virtue and Vice are present
    2. Mantle merit appears exactly once for the court in their tags
    3. The Unseen Sense merit must not be present

    Missing or incorrect notes can be fixed automatically if desired.

    Args:
        character (dict): Character data to lint
        fix (bool): Whether to automatically correct certain problems
        strict (bool): Whether to report non-critical errors and omissions
        sk_data (dict): Seeming and kith data, as from the
            settings/settings-changeling.json file.

    Returns:
        List of problem descriptions. If no problems were found, the list will
        be empty.
    """
    problems = []
    dirty = False

    if character.type_key != 'changeling':
        problems.append('Attempting to lint non-changeling character using changeling linter')
        return problems

    # Check that seeming tag exists and is valid
    for seeming_name in character.tags('seeming'):
        if seeming_name.lower() not in sk_data['seemings']:
            problems.append("Unrecognized @seeming '{}'".format(seeming_name))

    # Check that kith tag exists and is valid
    all_kiths = flatten(sk_data['kiths'].values())
    for kith_name in character.tags('kith'):
        if kith_name.lower() not in all_kiths:
            problems.append("Unrecognized @kith '{}'".format(kith_name))

    # If the character has no sheet, we're done
    if not character.path:
        return problems

    # Load the sheet for deep linting
    with open(character.path, 'r') as char_file:
        data = char_file.read()

    # STRICT: Check that they have a virtue and a vice
    if strict:
        problems.extend(nwod.lint_vice_virtue(data))

    # Get court for later
    court = character.tags('court').first_value()
    if not court:
        court = 'none'

    # Check that the mantle matches the court if given
    court_key = court.lower()
    mantle_courts = _get_mantle(data)
    mantle_court_keys = [c.lower() for c in mantle_courts]
    if mantle_courts:
        if len(mantle_courts) > 1:
            problems.append("Multiple mantle merits: {}".format(', '.join(mantle_courts)))
        elif court_key != mantle_court_keys[0]:
            problems.append("Court mantle '{}' does not match court tag '{}'".format(mantle_courts[0], court))

    # Check that goodwill does not match the character's own court or mantle
    goodwill_courts = _get_goodwill(data)
    goodwill_court_keys = [c.lower() for c in goodwill_courts]
    if goodwill_courts:
        if court_key in goodwill_court_keys:
            problems.append("Court goodwill listed for court tag '{}'".format(court))
        if mantle_courts and mantle_court_keys[0] in goodwill_court_keys:
            problems.append("Court goodwill listed for court mantle '{}'".format(mantle_courts[0]))

    # STRICT: Check that they have a mantle for their court
    if strict and court and court_key not in mantle_court_keys:
        problems.append("No mantle for court '{}'".format(court))

    # STRICT: Check that they do not have the Unseen Sense merit
    unseen_sense = _get_unseen_sense(data)
    if strict and unseen_sense:
        problems.append("Changelings cannot have the Unseen Sense merit")

    # Check that seeming tag matches listed seeming with correct notes
    seeming_tags = [t.lower() for t in character.tags['seeming']]
    if seeming_tags:
        # ensure the listed seemings match our seeming tags
        seeming_re = re.compile(
            SEEMING_REGEX.format(r'\w+'),
            re.MULTILINE | re.IGNORECASE
        )
        seeming_matches = list(seeming_re.finditer(data))
        seeming_stat_names = [m.group('seeming').lower() for m in seeming_matches]
        if set(seeming_tags) != set(seeming_stat_names):
            problems.append("Seeming stats do not match @seeming tags")
            if (len(seeming_stat_names) == 1
                    and len(seeming_tags) == 1
                    and seeming_stat_names[0] in REPLACEABLE):
                if fix:
                    seeming_tag = seeming_tags[0]
                    try:
                        seeming_parts = {
                            'title': seeming_tag.title(),
                            'seeming': sk_data['blessings'][seeming_tag],
                            'kith': sk_data['curses'][seeming_tag]
                        }
                        seeming_line = "{title} ({seeming}; {kith})".format(**seeming_parts)
                    except IndexError:
                        seeming_line = seeming_tag.title()

                    data = seeming_re.sub(
                        r'\g<1>{}'.format(seeming_line),
                        data
                    )
                    problems[-1] += ' (placeholder; FIXED)'
                    dirty = True
                else:
                    problems[-1] += ' (placeholder; can fix)'
        else:
            # Tags and stats match. Iterate through each seeming and make sure
            # the notes are right.
            for match in list(seeming_matches):
                seeming_tag = match.group('seeming').lower()
                if not seeming_tag in sk_data['seemings']:
                    continue

                loaded_seeming_notes = match.group('notes')
                seeming_notes = "({}; {})".format(sk_data['blessings'][seeming_tag], sk_data['curses'][seeming_tag])
                if not loaded_seeming_notes:
                    problems.append("Missing notes for Seeming '{}'".format(match.group('seeming')))
                    if fix:
                        data = _fix_seeming_notes(match.group('seeming'), seeming_notes, data)
                        problems[-1] += ' (FIXED)'
                        dirty = True
                    else:
                        problems[-1] += ' (can fix)'
                else:
                    if loaded_seeming_notes != seeming_notes:
                        problems.append("Incorrect notes for Seeming '{}'".format(match.group('seeming')))
                        if fix:
                            data = _fix_seeming_notes(match.group('seeming'), seeming_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'


    # Check that kith tag matches listed kith with correct notes
    kith_tags = [t.lower() for t in character.tags['kith']]
    if kith_tags:
        # ensure the listed kiths match our kith tags
        kith_re = re.compile(
            KITH_REGEX.format(r'\w+( \w+)?'),
            re.MULTILINE | re.IGNORECASE
        )
        kith_matches = list(kith_re.finditer(data))
        kith_stat_names = [m.group('kith').lower() for m in kith_matches]
        if set(kith_tags) != set([m.group('kith').lower() for m in kith_matches]):
            problems.append("Kith stats do not match @kith tags")
            if (len(kith_stat_names) == 1
                    and len(kith_tags) == 1
                    and kith_stat_names[0] in REPLACEABLE):
                if fix:
                    kith_tag = kith_tags[0]
                    try:
                        kith_line = "{} ({})".format(kith_tag.title(), sk_data['blessings'][kith_tag])
                    except IndexError:
                        kith_line = kith_tag.title()

                    data = kith_re.sub(
                        r'\g<1>{}'.format(kith_line),
                        data
                    )
                    problems[-1] += ' (placeholder; FIXED)'
                    dirty = True
                else:
                    problems[-1] += ' (placeholder; can fix)'
        else:
            # tags and stats match. iterate through each kith and make sure the
            # notes are right
            for match in list(kith_matches):
                kith_tag = match.group('kith').lower()
                if not kith_tag in sk_data['kiths'][seeming_tag]:
                    continue

                loaded_kith_notes = match.group('notes')
                kith_notes = "({})".format(sk_data['blessings'][kith_tag])
                if not loaded_kith_notes:
                    problems.append("Missing notes for Kith '{}'".format(match.group('kith')))
                    if fix:
                        data = _fix_kith_notes(match.group('kith'), kith_notes, data)
                        problems[-1] += ' (FIXED)'
                        dirty = True
                    else:
                        problems[-1] += ' (can fix)'
                else:
                    if loaded_kith_notes != kith_notes:
                        problems.append("Incorrect notes for Kith '{}'".format(match.group('kith')))
                        if fix:
                            data = _fix_kith_notes(match.group('kith'), kith_notes, data)
                            problems[-1] += ' (FIXED)'
                            dirty = True
                        else:
                            problems[-1] += ' (can fix)'

    if dirty and data:
        with open(character.path, 'w') as char_file:
            char_file.write(data)

    return problems

def _fix_seeming_notes(seeming, notes, data):
    """
    Insert correct notes for a seeming stat

    Args:
        seeming (str): Seeming name
        notes (str): New seeming notes
        data (str): Existing raw caracter data

    Returns
        Altered string character data with the new notes inserted
    """
    seeming_fix_re = re.compile(
        SEEMING_REGEX.format(seeming),
        re.MULTILINE | re.IGNORECASE
    )
    return seeming_fix_re.sub(
        r'\g<1>\g<2> {}'.format(notes),
        data
    )

def _fix_kith_notes(kith, notes, data):
    """
    Insert correct notes for a kith stat

    Args:
        kith (str): Kith name
        notes (str): New kith notes
        data (str): Existing raw caracter data

    Returns
        Altered string character data with the new notes inserted
    """
    kith_fix_re = re.compile(
        KITH_REGEX.format(kith),
        re.MULTILINE | re.IGNORECASE
    )
    return kith_fix_re.sub(
        r'\g<1>\g<2> {}'.format(notes),
        data
    )

def _get_mantle(data):
    std_mantle_re = re.compile(
        STANDARD_MANTLE_REGEX,
        re.MULTILINE | re.IGNORECASE
    )
    alt_mantle_re = re.compile(
        ALT_MANTLE_REGEX,
        re.MULTILINE | re.IGNORECASE
    )

    std_matches = std_mantle_re.finditer(data)
    alt_matches = alt_mantle_re.finditer(data)
    return [m.group('court') for m in flatten([std_matches, alt_matches])]

def _get_goodwill(data):
    std_goodwill_re = re.compile(
        STANDARD_GOODWILL_REGEX,
        re.MULTILINE | re.IGNORECASE
    )
    alt_goodwill_re = re.compile(
        ALT_GOODWILL_REGEX,
        re.MULTILINE | re.IGNORECASE
    )

    std_matches = std_goodwill_re.finditer(data)
    alt_matches = alt_goodwill_re.finditer(data)
    return [m.group('court') for m in flatten([std_matches, alt_matches])]

def _get_unseen_sense(data):
    merit_re = re.compile(
        UNSEEN_SENSE_REGEX,
        re.MULTILINE | re.IGNORECASE
    )

    return [m.group('thing') for m in merit_re.finditer(data)]
