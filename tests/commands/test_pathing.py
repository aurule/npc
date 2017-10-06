"""
Test the nuances of the npc.commands.util.create_path_from_character method
"""

import npc
from npc.commands import util

import pytest

def test_literal_component(tmpdir):
    char = npc.Character(type=['human'])
    tmpdir.mkdir('Dudes')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='Dudes')
    assert result == str(tmpdir.join('Dudes'))

def test_tag_presence_false(tmpdir):
    char = npc.Character(type=['human'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{school?Bros}')
    assert result == str(tmpdir)

def test_tag_presence_true(tmpdir):
    char = npc.Character(type=['human'], school=['u of bros'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{school?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_group_presence_true(tmpdir):
    char = npc.Character(type=['human'], groups=['some frat'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{groups?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_foreign_presence_true(tmpdir):
    char = npc.Character(type=['human'], foreign=['over there'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{foreign?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_wanderer_presence_true(tmpdir):
    """The foreign? check should include wanderer tag contents"""
    char = npc.Character(type=['human'], wanderer=[''])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{foreign?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_type_presence_true(tmpdir):
    char = npc.Character(type=['human'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{type?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_ranks_presence_true(tmpdir):
    char = npc.Character(type=['human'], ranks={'some frat': ['handstand guy']})
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{ranks?Bros}')
    assert result == str(tmpdir.join('Bros'))

def test_translated_presence_true(tmpdir):
    char = npc.Character(type=['changeling'], motley=['Kickasso'])
    tmpdir.mkdir('Bros')
    result = util.create_path_from_character(char, base_path=str(tmpdir), heirarchy='{type-unit?Bros}')
    assert result == str(tmpdir.join('Bros'))
