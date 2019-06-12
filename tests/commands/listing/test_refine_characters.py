"""Tests the behavior of certain special tags and directives"""

import npc
import pytest
import json

from npc.commands.listing import _refine_characters
from npc.character import Character

def test_characters_with_skip_are_excluded():
    c1 = Character(type=['human'])
    c2 = Character(type=['human'], skip=True)

    charlist = list(_refine_characters([c1, c2]))

    assert c1 in charlist
    assert c2 not in charlist

def test_faketype_replaces_type():
    c1 = Character(type=['vampire'], faketype=['human'])

    charlist = list(_refine_characters([c1]))

    assert charlist[0].tags('type').first_value() == 'human'

def test_hidden_tags_are_removed():
    c1 = Character(type=['human'], location=['France'])
    c1.tags('location').hidden = True

    charlist = list(_refine_characters([c1]))

    assert not c1.tags('location').present

def test_hidden_flags_are_removed():
    c1 = Character(type=['human'], foreign=['France'])
    c1.tags('foreign').hidden = True

    charlist = list(_refine_characters([c1]))

    assert not c1.tags('foreign').present

@pytest.mark.xfail
def test_hide_group(list_json_output):
    """The groups named in @hidegroup should not appear"""

    listing = list_json_output('hidegroup')
    assert 'Lawbros' not in listing[0]['group']

@pytest.mark.xfail
def test_hide_ranks(list_json_output):
    """The ranks for the groups named in @hiderank should not appear"""

    listing = list_json_output('hideranks')
    assert 'Big Corporation Place Thing' not in listing[0]['rank']

def test_missing_type_gets_default():
    c1 = Character()
    charlist = list(_refine_characters([c1]))
    assert c1.tags('type').first_value() == 'Unknown'
