import npc
import pytest

class TestBasicValidation:
    """Tests universal validations"""

    def test_blank_description(self):
        char = npc.Character(description='')
        char.validate()
        assert 'Missing description' in char.problems

    def test_whitespace_description(self):
        char = npc.Character(description=' \t')
        char.validate()
        assert 'Missing description' in char.problems

    required_tags = ('type', 'name')
    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_presence(self, tag):
        char = npc.Character(**{tag: []})
        char.validate()
        assert 'Missing {}'.format(tag) in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_whitespace(self, tag):
        char = npc.Character(**{tag: [' \t']})
        char.validate()
        assert 'Empty {}'.format(tag) in char.problems

    def test_multiple_types(self):
        char = npc.Character(type=['dog', 'cat'])
        char.validate(strict=True)
        assert "Multiple types: dog, cat" in char.problems

    def test_unknown_tags(self):
        """Unrecognized tags should be errors with strict validation"""
        char = npc.Character(head=['attached', 'bald'])
        char.validate(strict=True)
        assert 'Unrecognized tags: head' in char.problems

    def test_tag_present(self):
        char = npc.Character(head=['attached'], limbs=[' \n'], torso=[])
        char.problems = []
        char.validate_tag_present_and_filled('head')
        assert len(char.problems) == 0
        char.validate_tag_present_and_filled('limbs')
        assert 'Empty limbs' in char.problems
        char.validate_tag_present_and_filled('torso')
        assert 'Missing torso' in char.problems

    def test_tag_too_many(self):
        char = npc.Character(head=['left', 'right', 'beeblebrox'])
        char.validate_tag_appears_once('head')
        assert 'Multiple heads: left, right, beeblebrox' in char.problems

class TestChangelingValidation:
    """Tests the changeling-specific validations"""

    required_tags = ('seeming', 'kith')
    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_presence(self, tag):
        char = npc.Character(type=['changeling'], **{tag: []})
        char.validate()
        assert 'Missing {}'.format(tag) in char.problems

    @pytest.mark.parametrize('tag', required_tags)
    def test_required_tag_whitespace(self, tag):
        char = npc.Character(type=['changeling'], **{tag: [' \t']})
        char.validate()
        assert 'Empty {}'.format(tag) in char.problems

    only_one = [
        ('court', ['summer', 'winter']),
        ('motley', ['townies', 'hillbillies']),
        ('entitlement', ['honorable knights', 'dishonorable knights'])
    ]
    @pytest.mark.parametrize('key, values', only_one)
    def test_many_courts(self, key, values):
        char = npc.Character(type=['changeling'], **{key: values})
        char.validate()
        assert 'Multiple {key}s: {vals}'.format(key=key, vals=", ".join(values)) in char.problems

class TestValid:
    """Tests for the correctness of the `valid` getter"""

    def test_initial_state(self):
        """Character should be invalid before first call to validate()"""
        char = npc.Character(type=['human'], description='hi there', name=['dude'])
        assert not char.valid
        char.validate()
        assert char.valid

    def test_with_errors(self):
        char = npc.Character()
        char.validate()
        assert not char.valid
