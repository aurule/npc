"""
Test the nuances of the npc.commands.util.create_path_from_character method
"""

import npc
from npc.commands import util

import pytest

class TestPathLiteral:
    """Test that character literals are added"""

    def test_literal_component(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('Dudes')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='Dudes')
        assert result == str(tmpdir.join('Dudes'))

class TestTagPresence:
    """Test that tag presence is checked correctly"""

    def test_tag_presence_false(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{school?Bros}')
        assert result == str(tmpdir)

    def test_tag_presence_true(self, tmpdir):
        char = npc.Character(type=['human'], school=['U of Bros'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{school?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_group_presence_true(self, tmpdir):
        char = npc.Character(type=['human'], groups=['some frat'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{groups?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_foreign_presence_true(self, tmpdir):
        char = npc.Character(type=['human'], foreign=['over there'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{foreign?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_wanderer_presence_true(self, tmpdir):
        """The foreign? check should include wanderer tag contents"""
        char = npc.Character(type=['human'], wanderer=[''])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{foreign?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_type_presence_true(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{type?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_ranks_presence_true(self, tmpdir):
        char = npc.Character(type=['human'], ranks={'some frat': ['handstand guy']})
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{ranks?Bros}')
        assert result == str(tmpdir.join('Bros'))

    def test_translated_presence_true(self, tmpdir):
        char = npc.Character(type=['changeling'], motley=['Kickasso'])
        tmpdir.mkdir('Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{type-unit?Bros}')
        assert result == str(tmpdir.join('Bros'))

class TestTagInsertion:
    """Test that tag values are inserted"""

    def test_tag_no_value(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('U of Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{school}')
        assert result == str(tmpdir)

    def test_tag_no_value(self, tmpdir):
        char = npc.Character(type=['human'], school=['U of Bros'])
        tmpdir.mkdir('U of Bros')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{school}')
        assert result == str(tmpdir.join('U of Bros'))

    def test_type_tag_value_substitution(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('Humans')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{type}')
        assert result == str(tmpdir.join('Humans'))

    def test_translated_tags(self, tmpdir):
        char = npc.Character(type=['changeling'], motley=['Kickasso'])
        tmpdir.mkdir('Kickasso')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{type-unit}')
        assert result == str(tmpdir.join('Kickasso'))

    def test_single_group(self, tmpdir):
        char = npc.Character(type=['human'], group=['First', 'Second'])
        tmpdir.mkdir('First')
        tmpdir.mkdir('First/Second')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{group}')
        assert result == str(tmpdir.join('First'))

    def test_group_rank(self, tmpdir):
        char = npc.Character(type=['human'], group=['First', 'Second'], rank={'First': ['A', 'B']})
        tmpdir.mkdir('First')
        tmpdir.mkdir('First/A')
        tmpdir.mkdir('First/B')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{group}/{ranks}')
        assert result == str(tmpdir.join('First').join('A'))

    def test_group_folders(self, tmpdir):
        char = npc.Character(type=['human'], group=['First', 'Second'])
        tmpdir.mkdir('First')
        tmpdir.mkdir('First/Second')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{groups}')
        assert result == str(tmpdir.join('First').join('Second'))

    def test_groups_and_ranks(self, tmpdir):
        char = npc.Character(type=['human'], group=['First', 'Second'], rank={'First': ['A', 'B']})
        tmpdir.mkdir('First')
        tmpdir.mkdir('First/Second')
        tmpdir.mkdir('First/A')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{groups+ranks}')
        assert result == str(tmpdir.join('First').join('A'))

    def test_location_exists_with_foreign(self, tmpdir):
        # location is tried first
        char = npc.Character(type=['human'], foreign=['way the heck over there'], location=['over here'])
        tmpdir.mkdir('over here')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{locations}')
        assert result == str(tmpdir.join('over here'))

    def test_location_not_exist_and_foreign(self, tmpdir):
        # foreign is tried second
        char = npc.Character(type=['human'], foreign=['way the heck over there'], location=['over here'])
        tmpdir.mkdir('way the heck over there')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{locations}')
        assert result == str(tmpdir.join('way the heck over there'))

    def test_configured_missing_value(self, tmpdir):
        char = npc.Character(type=['changeling'])
        tmpdir.mkdir('Courtless')
        result = util.create_path_from_character(char, base_path=str(tmpdir), hierarchy='{type-social}')
        assert result == str(tmpdir.join('Courtless'))
