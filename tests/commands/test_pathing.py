"""
Test the nuances of the npc.commands.util.create_path_from_character method
"""

import npc
from npc.commands import util
from npc.character import Character

import pytest

class TestPathLiteral:
    """Test that character literals are added"""

    def test_literal_component(self, tmp_path):
        char = Character(type=['human'])
        tmp_path.joinpath('Dudes').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='Dudes')
        assert result == tmp_path.joinpath('Dudes')

class TestTagPresence:
    """Test that tag presence is checked correctly"""

    def test_tag_presence_false(self, tmp_path):
        char = Character(type=['human'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{school?Bros}')
        assert result == tmp_path

    def test_tag_presence_true(self, tmp_path):
        char = Character(type=['human'], school=['U of Bros'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{school?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_group_presence_true(self, tmp_path):
        char = Character(type=['human'], groups=['some frat'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{groups?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_foreign_presence_true(self, tmp_path):
        char = Character(type=['human'], foreign=['over there'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{foreign?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_wanderer_presence_true(self, tmp_path):
        """The foreign? check should include wanderer tag contents"""
        char = Character(type=['human'], wanderer=[''])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{foreign?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_type_presence_true(self, tmp_path):
        char = Character(type=['human'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{type?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_ranks_presence_true(self, tmp_path):
        char = Character(type=['human'], ranks={'some frat': ['handstand guy']})
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{ranks?Bros}')
        assert result == tmp_path.joinpath('Bros')

    def test_translated_presence_true(self, tmp_path):
        char = Character(type=['changeling'], motley=['Kickasso'])
        tmp_path.joinpath('Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{type-unit?Bros}')
        assert result == tmp_path.joinpath('Bros')

class TestTagInsertion:
    """Test that tag values are inserted"""

    def test_tag_no_value(self, tmp_path):
        char = Character(type=['human'])
        tmp_path.joinpath('U of Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{school}')
        assert result == tmp_path

    def test_tag_no_value(self, tmp_path):
        char = Character(type=['human'], school=['U of Bros'])
        tmp_path.joinpath('U of Bros').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{school}')
        assert result == tmp_path.joinpath('U of Bros')

    def test_type_tag_value_substitution(self, tmp_path):
        char = Character(type=['human'])
        tmp_path.joinpath('Humans').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{type}')
        assert result == tmp_path.joinpath('Humans')

    def test_translated_tags(self, tmp_path):
        char = Character(type=['changeling'], motley=['Kickasso'])
        tmp_path.joinpath('Kickasso').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{type-unit}')
        assert result == tmp_path.joinpath('Kickasso')

    def test_single_group(self, tmp_path):
        char = Character(type=['human'], group=['First', 'Second'])
        first = tmp_path / 'First'
        first.mkdir()
        second = first / 'Second'
        second.mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{group}')
        assert result == tmp_path.joinpath('First')

    def test_group_rank(self, tmp_path):
        char = Character(type=['human'], group=['First', 'Second'], rank={'First': ['A', 'B']})
        first = tmp_path / 'First'
        first.mkdir()
        first.joinpath('A').mkdir()
        first.joinpath('B').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{group}/{ranks}')
        assert result == tmp_path.joinpath('First').joinpath('A')

    def test_group_folders(self, tmp_path):
        char = Character(type=['human'], group=['First', 'Second'])
        first = tmp_path / 'First'
        first.mkdir()
        second = first / 'Second'
        second.mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{groups}')
        assert result == tmp_path.joinpath('First').joinpath('Second')

    def test_groups_and_ranks(self, tmp_path):
        char = Character(type=['human'], group=['First', 'Second'], rank={'First': ['A', 'B']})
        first = tmp_path / 'First'
        first.mkdir()
        second = first / 'Second'
        second.mkdir()
        third = first / 'A'
        third.mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{groups+ranks}')
        assert result == tmp_path.joinpath('First').joinpath('A')

    def test_location_exists_with_foreign(self, tmp_path):
        # location is tried first
        char = Character(type=['human'], foreign=['way the heck over there'], location=['over here'])
        tmp_path.joinpath('over here').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{locations}')
        assert result == tmp_path.joinpath('over here')

    def test_location_not_exist_and_foreign(self, tmp_path):
        # foreign is tried second
        char = Character(type=['human'], foreign=['way the heck over there'], location=['over here'])
        tmp_path.joinpath('way the heck over there').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{locations}')
        assert result == tmp_path.joinpath('way the heck over there')

    def test_configured_missing_value(self, tmp_path):
        char = Character(type=['changeling'])
        tmp_path.joinpath('Courtless').mkdir()
        result = util.create_path_from_character(char, base_path=tmp_path, hierarchy='{type-social}')
        assert result == tmp_path.joinpath('Courtless')
