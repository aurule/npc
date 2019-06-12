import re
import npc
from npc.character.tags import TagContainer
from npc.character import Character
from mako.template import Template

def template_output(character, header_level=3):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.markdown.character.default'))
    character_template = Template(filename=template_path)
    return character_template.render(tags=character.tags, header_level=header_level)

def test_inserts_hashes_for_header_level():
    char = Character()
    output = template_output(char, 3)
    assert re.match(r'^###', output) is not None

class TestName:
    def test_uses_first_name_for_header(self):
        char = Character()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '# Joe Smith' in output

    def test_adds_aka_for_remaining_names(self):
        char = Character()
        char.tags('name').extend(['Joe Smith', 'Mr. Smith', 'The Man'])
        output = template_output(char)
        assert '*AKA Mr. Smith, The Man*' in output

class TestDead:
    def test_inserts_deceased_note_if_dead(self):
        char = Character()
        char.tags('name').append('Joe Smith')
        char.tags('dead').touch()
        output = template_output(char)
        assert '# Joe Smith (Deceased)' in output

    def test_no_dead_section_without_dead_notes(self):
        char = Character()
        char.tags('name').append('Joe Smith')
        output = template_output(char)
        assert '*Dead:*' not in output

    def test_has_dead_section_with_dead_notes(self):
        char = Character()
        char.tags('name').append('Joe Smith')
        char.tags('dead').append('fell hard')
        output = template_output(char)
        assert '*Dead:* fell hard' in output

def test_titles_on_own_line():
    char = Character()
    char.tags('title').extend(['title 1', 'title 2'])
    output = template_output(char)
    assert re.search(r'^title 1, title 2$', output, re.MULTILINE) is not None

def test_types_separated_with_slash():
    char = Character()
    char.tags('type').extend(['human', 'changeling'])
    output = template_output(char)
    assert 'human/changeling' in output

def test_locations_appended_to_types():
    char = Character()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').append('florida')
    char.tags('location').append('orlando')
    output = template_output(char)
    assert 'human/changeling in florida and orlando' in output

def test_foreign_note_if_foreign():
    char = Character()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    output = template_output(char)
    assert 'human/changeling (foreign)' in output

def test_wanderer_note_if_wanderer():
    char = Character()
    char.tags('type').extend(['human', 'changeling'])
    char.tags('foreign').touch()
    char.tags('wanderer').touch()
    output = template_output(char)
    assert 'human/changeling (foreign), Wanderer' in output

class TestGroups:
    def test_first_group_is_inline_with_type(self):
        char = Character()
        char.tags('type').append('human')
        char.tags('group').append('student council')
        output = template_output(char)
        assert re.search(r'human.*, student council', output) is not None

    def test_first_group_tags_appended(self):
        char = Character()
        char.tags('type').append('human')
        char.tags('group').append('student council')
        char.tags('group').subtag('student council').append('president')
        char.tags('group').subtag('student council').append('member')
        output = template_output(char)
        assert re.search(r'human.*, student council \(president, member\)', output) is not None

    def test_remaining_groups_in_own_section(self):
        char = Character()
        char.tags('type').append('human')
        char.tags('group').append('student council')
        char.tags('group').subtag('student council').append('president')
        char.tags('group').subtag('student council').append('member')
        char.tags('group').append('volleyball')
        char.tags('group').subtag('volleyball').append('star')
        char.tags('group').append('chess club')
        char.tags('group').subtag('chess club').append('newbie')
        output = template_output(char)
        assert re.search(r'^volleyball \(star\), chess club \(newbie\)$', output, re.MULTILINE) is not None

def test_first_motley_inline_with_type():
    char = Character()
    char.tags('type').append('human')
    char.tags.add_group('motley', 'weirdos')
    char.tags('motley').subtag('weirdos').append('token bro')
    output = template_output(char)
    assert re.search(r'human.*, weirdos Motley \(token bro\)$', output, re.MULTILINE) is not None

def test_group_then_motley():
    char = Character()
    char.tags('type').append('human')
    char.tags.add_group('motley', 'weirdos')
    char.tags('motley').subtag('weirdos').append('token bro')
    char.tags('group').append('student council')
    char.tags('group').subtag('student council').append('president')
    output = template_output(char)
    assert re.search(r'human.*student council \(president\), weirdos Motley \(token bro\)$', output, re.MULTILINE) is not None

class TestAppearance:
    def test_has_section_if_filled(self):
        char = Character()
        char.tags('appearance').append('grungy')
        output = template_output(char)
        assert re.search(r'^\*Appearance:\* grungy$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Character()
        output = template_output(char)
        assert '*Appearance:*' not in output

class TestDescription:
    def test_has_section_if_filled(self):
        char = Character()
        char.tags('description').append('some guy')
        output = template_output(char)
        assert re.search(r'^\*Notes:\* some guy$', output, re.MULTILINE) is not None

    def test_no_section_if_not_filled(self):
        char = Character()
        output = template_output(char)
        assert '*Notes:*' not in output

def test_full_sheet_formatting():
    char = Character()
    char.tags('type').append('Human')
    char.tags('name').extend(['Bob Herbson', 'Bobbie'])
    char.tags('dead').append('Perished in a teleporter accident.')
    char.tags('title').append('The Human Guinea Pig')
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
### Bob Herbson (Deceased)

*AKA Bobbie*
The Human Guinea Pig
Human in Moontown, Wanderer, Testers (Chief Marshall), Moon Morons Motley (Fixer)
Croquet Team (Water Boy)

*Appearance:* Red shirt and a goofy grin.

*Notes:* Outgoing fella with a shady hobby and no fear of death.

*Dead:* Perished in a teleporter accident.

"""
    assert output == expected
