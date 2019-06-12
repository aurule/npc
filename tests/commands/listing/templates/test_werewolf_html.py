import re
import npc
from npc.character.tags import TagContainer
from npc.character import Werewolf
from mako.template import Template
from markdown import Markdown

def template_output(character, header_level=3):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.html.character.werewolf'))
    character_template = Template(filename=template_path)
    md_converter = Markdown(extensions=['markdown.extensions.smarty'])
    _clean_conv = md_converter.reset
    return character_template.render(tags=character.tags, header_level=header_level, mdconv=_clean_conv().convert)

def test_inserts_hashes_for_header_level():
    char = Werewolf()
    output = template_output(char, 3)
    assert re.match(r'^<h3>.*</h3>', output) is not None

class TestName:
    def test_uses_first_name_for_header(self):
        char = Werewolf()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '<h3>Joe Smith</h3>' in output

    def test_adds_aka_for_remaining_names(self):
        char = Werewolf()
        char.tags('name').extend(['Joe Smith', 'Mr. Smith', 'The Man'])
        output = template_output(char)
        assert '<div><em>AKA Mr. Smith, The Man</em></div>' in output

class TestDead:
    def test_inserts_deceased_note_if_dead(self):
        char = Werewolf()
        char.tags('name').append('Joe Smith')
        char.tags('dead').touch()
        output = template_output(char)
        assert '<h3>Joe Smith (Deceased)</h3>' in output

    def test_no_dead_section_without_dead_notes(self):
        char = Werewolf()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '<em>Dead:</em>' not in output

    def test_has_dead_section_with_dead_notes(self):
        char = Werewolf()
        char.tags('name').append('Joe Smith')
        char.tags('dead').append('fell hard')
        output = template_output(char)
        assert '<em>Dead:</em> fell hard' in output

def test_titles_on_own_line():
    char = Werewolf()
    char.tags('title').extend(['title 1', 'title 2'])
    output = template_output(char)
    assert re.search(r'^<div>title 1, title 2</div>$', output, re.MULTILINE) is not None

def test_types_separated_with_slash():
    char = Werewolf()
    char.tags('type').extend(['human', 'changeling'])
    output = template_output(char)
    assert 'human/changeling' in output

def test_locations_appended_to_types():
    char = Werewolf()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').append('florida')
    char.tags('location').append('orlando')
    output = template_output(char)
    assert 'human/changeling in florida and orlando' in output

def test_foreign_note_if_foreign():
    char = Werewolf()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    output = template_output(char)
    assert 'human/changeling (foreign)' in output

def test_wanderer_note_if_wanderer():
    char = Werewolf()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    char.tags('wanderer').touch()
    output = template_output(char)
    assert 'human/changeling (foreign), Wanderer' in output

class TestPack:
    def test_first_pack_on_own_line(self):
        char = Werewolf()
        char.tags('pack').append('grinners')
        output = template_output(char)
        assert '<br />grinners Pack' in output

    def test_pack_rank_included(self):
        char = Werewolf()
        char.tags('pack').append('grinners')
        char.tags('pack').subtag('grinners').append('scout')
        output = template_output(char)
        assert 'grinners Pack (scout)' in output

class TestTribe:
    def test_first_tribe_appears_with_pack(self):
        char = Werewolf()
        char.tags('pack').append('Grinners')
        char.tags('tribe').append('Blood Talons')
        output = template_output(char)
        assert 'Grinners Pack, Blood Talons Tribe' in output

    def test_missing_tribe_yields_ghost_wolf(self):
        char = Werewolf()
        char.tags('pack').append('Grinners')
        output = template_output(char)
        assert 'Grinners Pack, Ghost Wolf' in output

def test_auspices_joined_with_slash():
    char = Werewolf()
    char.tags('auspice').extend(['Rahu', 'Cahalith'])
    output = template_output(char)
    assert 'Rahu/Cahalith' in output

def test_lodge_in_own_section():
    char = Werewolf()
    char.tags('lodge').append('Sky Splitters')
    char.tags('lodge').subtag('Sky Splitters').append('Dancer')
    output = template_output(char)
    assert '<div>Sky Splitters (Dancer)</div>' in output

def test_all_groups_in_own_section():
    char = Werewolf()
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

class TestAppearance:
    def test_has_section_if_filled(self):
        char = Werewolf()
        char.tags('appearance').append('grungy')
        output = template_output(char)
        assert re.search(r'^<p><em>Appearance:</em> grungy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Werewolf()
        output = template_output(char)
        assert '<em>Appearance:</em>' not in output

class TestDescription:
    def test_has_section_if_filled(self):
        char = Werewolf()
        char.tags('description').append('some guy')
        output = template_output(char)
        assert re.search(r'^<p><em>Notes:</em> some guy</p>$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Werewolf()
        output = template_output(char)
        assert '<em>Notes:</em>' not in output

def test_full_sheet_formatting():
    char = Werewolf()
    char.tags('name').extend(['Bob Herbson', 'Bobbie'])
    char.tags('dead').append('Perished in a teleporter accident.')
    char.tags('title').append('The Werewolf Guinea Pig')
    char.tags('pack').append("Mama's Boys")
    char.tags('tribe').append('Glass Walkers')
    char.tags('auspice').append('Irraka')
    char.tags('lodge').append('Oedipus Lets')
    char.tags('location').append('Moontown')
    char.tags('wanderer').touch()
    char.tags('group').append('Testers')
    char.tags('group').subtag('Testers').append('Chief Marshall')
    char.tags('group').append('Croquet Team')
    char.tags('group').subtag('Croquet Team').append('Water Boy')
    char.tags.add_group('motley', 'Moon Morons')
    char.tags('motley').subtag('Moon Morons').append('Fixer')
    char.tags('appearance').append('Red shirt and a goofy grin.')
    char.tags('description').append('Outgoing fella with a shady hobby and no fear of death.')
    output = template_output(char)
    print(output) # Always print the real output for when things go wrong
    expected = """\
<h3>Bob Herbson (Deceased)</h3>

<div><em>AKA Bobbie</em></div>
<div>The Werewolf Guinea Pig</div>
<div>werewolf in Moontown, Wanderer
<br />Mama's Boys Pack, Glass Walkers Tribe</div>
<div>Irraka</div>
<div>Oedipus Lets</div>
<div>Testers (Chief Marshall), Croquet Team (Water Boy)</div>
<p><em>Appearance:</em> Red shirt and a goofy grin.</p>
<p><em>Notes:</em> Outgoing fella with a shady hobby and no fear of death.</p>
<p><em>Dead:</em> Perished in a teleporter accident.</p>
"""
    assert output == expected
