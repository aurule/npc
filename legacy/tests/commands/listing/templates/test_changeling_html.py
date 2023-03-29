import re
import npc
from npc.character.tags import TagContainer
from npc.character import Changeling
from mako.template import Template
from markdown import Markdown

def template_output(character, header_level=3):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.html.character.changeling'))
    character_template = Template(filename=template_path)
    md_converter = Markdown(extensions=['markdown.extensions.smarty'])
    _clean_conv = md_converter.reset
    return character_template.render(tags=character.tags, header_level=header_level, mdconv=_clean_conv().convert)

def test_inserts_hashes_for_header_level():
    char = Changeling()
    output = template_output(char, 3)
    assert re.match(r'^<h3>.*</h3>', output) is not None

class TestName:
    def test_uses_first_name_for_header(self):
        char = Changeling()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '<h3>Joe Smith</h3>' in output

    def test_adds_aka_for_remaining_names(self):
        char = Changeling()
        char.tags('name').extend(['Joe Smith', 'Mr. Smith', 'The Man'])
        output = template_output(char)
        assert '<div><em>AKA Mr. Smith, The Man</em></div>' in output

class TestDead:
    def test_inserts_deceased_note_if_dead(self):
        char = Changeling()
        char.tags('name').append('Joe Smith')
        char.tags('dead').touch()
        output = template_output(char)
        assert '<h3>Joe Smith (Deceased)</h3>' in output

    def test_no_dead_section_without_dead_notes(self):
        char = Changeling()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '<em>Dead:</em>' not in output

    def test_has_dead_section_with_dead_notes(self):
        char = Changeling()
        char.tags('name').append('Joe Smith')
        char.tags('dead').append('fell hard')
        output = template_output(char)
        assert '<em>Dead:</em> fell hard' in output

def test_titles_on_own_line():
    char = Changeling()
    char.tags('title').extend(['title 1', 'title 2'])
    output = template_output(char)
    assert re.search(r'^<div>title 1, title 2</div>$', output, re.MULTILINE) is not None

def test_types_separated_with_slash():
    char = Changeling()
    char.tags('type').extend(['human', 'changeling'])
    output = template_output(char)
    assert 'human/changeling' in output

def test_locations_appended_to_types():
    char = Changeling()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').append('florida')
    char.tags('location').append('orlando')
    output = template_output(char)
    assert 'human/changeling in florida and orlando' in output

def test_foreign_note_if_foreign():
    char = Changeling()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    output = template_output(char)
    assert 'human/changeling (foreign)' in output

def test_wanderer_note_if_wanderer():
    char = Changeling()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    char.tags('wanderer').touch()
    output = template_output(char)
    assert 'human/changeling (foreign), Wanderer' in output

def test_all_groups_in_own_section():
    char = Changeling()
    char.tags('type').append('human')
    char.tags('group').append('student council')
    char.tags('group').subtag('student council').append('president')
    char.tags('group').subtag('student council').append('member')
    char.tags('group').append('volleyball')
    char.tags('group').subtag('volleyball').append('star')
    char.tags('group').append('chess club')
    char.tags('group').subtag('chess club').append('newbie')
    output = template_output(char)
    assert '<div>student council (president, member), volleyball (star), chess club (newbie)</div>' in output

class TestMotley:
    def test_first_motley_inline_with_type(self):
        char = Changeling()
        char.tags('motley').append('weirdos')
        char.tags('motley').subtag('weirdos').append('token bro')
        output = template_output(char)
        assert re.search(r'changeling.*, weirdos Motley \(token bro\)', output, re.MULTILINE) is not None

class TestCourt:
    def test_first_court_inline_with_type(self):
        char = Changeling()
        char.tags('court').append('North')
        char.tags('court').subtag('North').append('token bro')
        output = template_output(char)
        assert re.search(r'changeling.*, North Court \(token bro\)', output, re.MULTILINE) is not None

    def test_courtless_with_no_court(self):
        char = Changeling()
        output = template_output(char)
        assert re.search(r'changeling.*, Courtless', output, re.MULTILINE) is not None

def test_freehold_inline_with_type():
    char = Changeling()
    char.tags('freehold').append('da club')
    output = template_output(char)
    assert re.search(r'changeling.*, Courtless \(da club\)', output, re.MULTILINE) is not None

class TestSeemingKith:
    def test_only_seeming_ends_line(self):
        char = Changeling()
        char.tags('seeming').append('Wizened')
        output = template_output(char)
        assert '<div>Wizened</div>' in output

    def test_only_kith_ends_line(self):
        char = Changeling()
        char.tags('kith').append('Drudge')
        output = template_output(char)
        assert '<div>Drudge</div>' in output

    def test_both_separates_with_space(self):
        char = Changeling()
        char.tags('seeming').append('Wizened')
        char.tags('kith').append('Drudge')
        output = template_output(char)
        assert '<div>Wizened Drudge</div>' in output

    def test_multiple_seemings_separated_with_slash(self):
        char = Changeling()
        char.tags('seeming').append('Wizened')
        char.tags('seeming').append('Elemental')
        output = template_output(char)
        assert 'Wizened/Elemental' in output

    def test_multiple_kiths_separated_with_slash(self):
        char = Changeling()
        char.tags('kith').append('Drudge')
        char.tags('kith').append('Artist')
        output = template_output(char)
        assert 'Drudge/Artist' in output

def test_entitlement_on_own_line():
    char = Changeling()
    char.tags('entitlement').append('Bros')
    output = template_output(char)
    assert '<div>Bros</div>' in output

class TestAppearance:
    def test_has_section_if_filled(self):
        char = Changeling()
        char.tags('appearance').append('grungy')
        output = template_output(char)
        assert re.search(r'^<p><em>Appearance:</em> grungy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Changeling()
        output = template_output(char)
        assert '<em>Appearance:</em>' not in output

class TestMien:
    def test_has_section_if_filled(self):
        char = Changeling()
        char.tags('mien').append('grungy')
        output = template_output(char)
        assert re.search(r'^<p><em>Mien:</em> grungy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Changeling()
        output = template_output(char)
        assert '*Mien:*' not in output

class TestMask:
    def test_has_section_if_filled(self):
        char = Changeling()
        char.tags('mask').append('grungy')
        output = template_output(char)
        assert re.search(r'^<p><em>Mask:</em> grungy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Changeling()
        output = template_output(char)
        assert '*Mask:*' not in output

class TestDescription:
    def test_has_section_if_filled(self):
        char = Changeling()
        char.tags('description').append('some guy')
        output = template_output(char)
        assert re.search(r'^<p><em>Notes:</em> some guy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Changeling()
        output = template_output(char)
        assert '<em>Notes:</em>' not in output

def test_full_sheet_formatting():
    char = Changeling()
    char.tags('name').extend(['Bob Herbson', 'Bobbie'])
    char.tags('seeming').append('Elemental')
    char.tags('kith').append('Fireheart')
    char.tags('motley').append('Reflectors')
    char.tags('court').append('Summer')
    char.tags('freehold').append('Lunar Essence')
    char.tags('entitlement').append("Sun's Proxies")
    char.tags('mien').append('Skin like red-hot bubbling pitch.')
    char.tags('mask').append('Always has a sunburn.')
    char.tags('dead').append('Perished in a teleporter accident.')
    char.tags('title').append('The Changeling Guinea Pig')
    char.tags('location').append('Moontown')
    char.tags('wanderer').touch()
    char.tags('group').append('Testers')
    char.tags('group').subtag('Testers').append('Chief Marshall')
    char.tags('group').append('Croquet Team')
    char.tags('group').subtag('Croquet Team').append('Water Boy')
    char.tags('motley').append('Moon Morons')
    char.tags('motley').subtag('Moon Morons').append('Fixer')
    char.tags('appearance').append('Red shirt and a goofy grin.')
    char.tags('description').append('Outgoing fella with a shady hobby and no fear of death.')
    output = template_output(char)
    print(output) # Always print the real output for when things go wrong
    expected = """\
<h3>Bob Herbson (Deceased)</h3>

<div><em>AKA Bobbie</em></div>
<div>The Changeling Guinea Pig</div>
<div>changeling in Moontown, Wanderer, Reflectors Motley, Summer Court (Lunar Essence)</div>
<div>Elemental Fireheart</div>
<div>Sun's Proxies</div>
<div>Testers (Chief Marshall), Croquet Team (Water Boy)</div>
<p><em>Appearance:</em> Red shirt and a goofy grin.</p>
<p><em>Mien:</em> Skin like red-hot bubbling pitch.</p>
<p><em>Mask:</em> Always has a sunburn.</p>
<p><em>Notes:</em> Outgoing fella with a shady hobby and no fear of death.</p>
<p><em>Dead:</em> Perished in a teleporter accident.</p>
"""
    assert output == expected
