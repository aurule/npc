import npc
import pytest
import os
import re

@pytest.fixture(scope="module")
def arglist():
    return [
        'changeling',
        'changeling mann',
        'Beast',
        'Hunterheart'
    ]

def test_creates_character(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist)
    result = npc.commands.create_changeling(args, prefs)
    character = campaign.get_character('changeling mann.nwod')
    assert result.success
    assert character.check()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_adds_group_tags(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist + ['-g', 'fork', 'spoon'])
    npc.commands.create_changeling(args, prefs)
    data = campaign.get_character_data('changeling mann.nwod')
    assert data['group'] == ['fork', 'spoon']

def test_duplicate_character(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist)
    npc.commands.create_changeling(args, prefs)
    result = npc.commands.create_changeling(args, prefs)
    assert not result.success

def test_adds_seeming(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist)
    npc.commands.create_changeling(args, prefs)
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Beast' in data['seeming']

def test_adds_seeming_notes(argparser, prefs, campaign, arglist):
    """Seeming notes should be added within the character file.

    This test does not ensure that the notes are correct."""

    args = argparser.parse_args(arglist)
    npc.commands.create_changeling(args, prefs)
    character = campaign.get_character('changeling mann.nwod')
    assert '    Seeming Beast (' in character.read()

def test_adds_kith(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist)
    npc.commands.create_changeling(args, prefs)
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Hunterheart' in data['kith']

def test_adds_kith_notes(argparser, prefs, campaign, arglist):
    """Kith notes should be added within the character file.

    This test does not ensure that the notes are correct."""

    args = argparser.parse_args(arglist)
    npc.commands.create_changeling(args, prefs)
    character = campaign.get_character('changeling mann.nwod')
    assert '    Kith    Hunterheart (' in character.read()

def test_adds_court(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist + ['--court', 'Summer'])
    npc.commands.create_changeling(args, prefs)
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Summer' in data['court']

def test_adds_court(argparser, prefs, campaign, arglist):
    args = argparser.parse_args(arglist + ['--motley', 'Funny Bones Men'])
    npc.commands.create_changeling(args, prefs)
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Funny Bones Men' in data['motley']
