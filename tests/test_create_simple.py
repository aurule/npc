import npc
import pytest
import os

@pytest.fixture(params=['human', 'fetch', 'goblin'])
def commandline(request):
    return ['g', 'testmann', request.param, '-g', 'fork', 'spoon']

def test_missing_template(argparser, campaign):
    args = argparser.parse_args(['g', 'noname', 'notfound'])
    result = npc.commands.create_simple(args)
    assert not result.success
    assert result.errcode == 7

def test_creates_character(argparser, campaign, commandline):
    args = argparser.parse_args(commandline)
    result = npc.commands.create_simple(args)
    character = campaign.get_character('testmann.nwod')
    assert result.success
    assert character.check()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_duplicate_character(argparser, campaign, commandline):
    args = argparser.parse_args(commandline)
    npc.commands.create_simple(args)
    result = npc.commands.create_simple(args)
    assert not result.success
    assert result.errcode == 1

def test_adds_group_tags(argparser, campaign, commandline):
    args = argparser.parse_args(commandline)
    npc.commands.create_simple(args)
    data = campaign.get_character_data('testmann.nwod')
    assert data['group'] == ['fork', 'spoon']

def test_adds_foreign_tag(argparser, campaign, commandline):
    """With just --foreign, add the tag and no notes"""
    commandline.extend(['--foreign', 'Lives on the moon, with Steve'])
    args = argparser.parse_args(commandline)
    npc.commands.create_simple(args)
    data = campaign.get_character_data('testmann.nwod')
    assert data['foreign'] == ['Lives on the moon, with Steve']

class TestDead:
    """Test permutations of the --dead arg"""

    def test_no_dead_tag(self, argparser, campaign, commandline):
        """Characters shouldn't be dead without the command"""
        args = argparser.parse_args(commandline)
        npc.commands.create_simple(args)
        data = campaign.get_character_data('testmann.nwod')
        assert 'dead' not in data

    def test_bare_dead_tag(self, argparser, campaign, commandline):
        """With just --dead, add the tag and no notes"""
        commandline.extend(['--dead'])
        args = argparser.parse_args(commandline)
        npc.commands.create_simple(args)
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['']

    def test_dead_tag_with_notes(self, argparser, campaign, commandline):
        """With just --dead, add the tag and no notes"""
        commandline.extend(['--dead', 'Died in a tragic toast accident'])
        args = argparser.parse_args(commandline)
        npc.commands.create_simple(args)
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['Died in a tragic toast accident']
