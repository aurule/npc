"""Tests universal validations"""

import npc
from npc.character import Character
import pytest

class TestDescription:
    def test_filled_description(self):
        char = Character(description='Hi there!')
        char.validate()
        assert 'Missing description' not in char.problems

    def test_blank_description(self):
        char = Character(description='')
        char.validate()
        assert 'Missing description' in char.problems

    def test_whitespace_description(self):
        char = Character(description=' \t')
        char.validate()
        assert 'Missing description' in char.problems

class TestRequiredTags:
    required_tags = ('type', 'name')

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_is_present(self, tag):
        char = Character(**{tag: ['foobar']})
        char.validate()
        assert 'Missing {}'.format(tag) not in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_not_present(self, tag):
        char = Character(**{tag: []})
        char.validate()
        assert 'Missing {}'.format(tag) in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_whitespace(self, tag):
        char = Character(**{tag: [' \t']})
        char.validate()
        assert 'Empty {}'.format(tag) in char.problems

class TestStrict:
    def test_single_type(self):
        char = Character(type=['dog'])
        char.validate(strict=True)
        assert "Multiple types" not in char.problems

    def test_multiple_types(self):
        char = Character(type=['dog', 'cat'])
        char.validate(strict=True)
        assert "Multiple types: dog, cat" in char.problems

    def test_unknown_tags(self):
        """Unrecognized tags should be errors with strict validation"""
        char = Character(head=['attached', 'bald'])
        char.validate(strict=True)
        assert 'Unrecognized tags: head' in char.problems

class TestHelpers:
    def test_tag_present_and_filled(self):
        char = Character(head=['attached'], limbs=[' \n'], torso=[])
        char.problems = []
        char.validate_tag_present_and_filled('head')
        assert len(char.problems) == 0
        char.validate_tag_present_and_filled('limbs')
        assert 'Empty limbs' in char.problems
        char.validate_tag_present_and_filled('torso')
        assert 'Missing torso' in char.problems

    def test_tag_appears_once(self):
        char = Character(head=['left', 'right', 'beeblebrox'])
        char.validate_tag_appears_once('head')
        assert 'Multiple heads: left, right, beeblebrox' in char.problems

class TestValid:
    """Tests for the correctness of the `valid` getter"""

    def test_initial_state(self):
        """Character should be invalid before first call to validate()"""
        char = Character(type=['human'], description='hi there', name=['dude'])
        assert not char.valid
        char.validate()
        assert char.valid

    def test_with_errors(self):
        char = Character()
        char.validate()
        assert not char.valid
