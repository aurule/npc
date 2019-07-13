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
        assert "No values for tag 'description'" in char.problems

    def test_whitespace_description(self):
        char = Character(description=' \t')
        char.validate()
        assert "No values for tag 'description'" in char.problems

class TestRequiredTags:
    required_tags = ('type', 'name')

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_is_present(self, tag):
        char = Character(**{tag: ['foobar']})
        char.validate()
        assert "No values for tag '{}'".format(tag) not in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_not_present(self, tag):
        char = Character(**{tag: []})
        char.validate()
        assert "No values for tag '{}'".format(tag) in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_whitespace(self, tag):
        char = Character(**{tag: [' \t']})
        char.validate()
        assert "No values for tag '{}'".format(tag) in char.problems

class TestStrict:
    def test_single_type(self):
        char = Character(type=['dog'])
        char.validate(strict=True)
        assert "Multiple types" not in char.problems

    def test_multiple_types(self):
        char = Character(type=['dog', 'cat'])
        char.validate(strict=True)
        assert "Too many values for tag 'type'. Limit of 1" in char.problems

    def test_unknown_tags(self):
        """Unrecognized tags should be errors with strict validation"""
        char = Character(head=['attached', 'bald'])
        char.validate(strict=True)
        assert "Unrecognized tag 'head'" in char.problems

    def test_nolint_without_skip(self):
        char = Character(nolint=True)
        char.validate(strict=True)
        assert 'Linting disabled, but character is visible in lists' in char.problems

class TestValid:
    """Tests for the correctness of the `valid` getter"""

    def test_initial_state(self):
        """Character should be invalid before first call to validate()"""
        char = Character(type=['human'], description='hi there', name=['dude'])
        assert not char.valid
        char.validate()
        print(char.problems)
        assert char.valid

    def test_with_errors(self):
        char = Character()
        char.validate()
        assert not char.valid

def test_wrong_class():
    char = Character(type=['changeling'])
    char.validate(strict=True)
    assert not char.valid
    assert "Incorrect type 'changeling' for class 'Character': implies class 'Changeling'" in char.problems
