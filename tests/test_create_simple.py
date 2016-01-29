import npc
import pytest
import os

@pytest.fixture(params=['human', 'fetch', 'goblin'])
def commandline(request):
    return ['g', 'testmann', request.param, '-g', 'fork', 'spoon']

def test_missing_template(argparser, prefs, campaign):
    args = argparser.parse_args(['g', 'noname', 'notfound'])
    result = npc.commands.create_simple(args, prefs)
    assert not result.success
    assert result.errcode == 7

def test_creates_character(argparser, prefs, campaign, commandline):
    args = argparser.parse_args(commandline)
    result = npc.commands.create_simple(args, prefs)
    character = campaign.get_character('testmann.nwod')
    assert result.success
    assert character.check()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_duplicate_character(argparser, prefs, campaign, commandline):
    args = argparser.parse_args(commandline)
    npc.commands.create_simple(args, prefs)
    result = npc.commands.create_simple(args, prefs)
    assert not result.success
    assert result.errcode == 1

def test_adds_group_tags(argparser, prefs, campaign, commandline):
    args = argparser.parse_args(commandline)
    npc.commands.create_simple(args, prefs)
    data = campaign.get_character_data('testmann.nwod')
    assert data['group'] == ['fork', 'spoon']
