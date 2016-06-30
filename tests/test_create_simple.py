import npc
import pytest
import os

@pytest.fixture(params=['human', 'fetch', 'goblin'])
def commandline(request):
    return ['g', 'testmann', request.param, '-g', 'fork', 'spoon']

def test_missing_template(campaign):
    result = npc.commands.create_simple('noname', 'notfound')
    assert not result.success
    assert result.errcode == 7

@pytest.mark.parametrize('chartype', ['human', 'fetch', 'goblin'])
def test_creates_character(campaign, chartype):
    result = npc.commands.create_simple('testmann', chartype)
    character = campaign.get_character('testmann.nwod')
    assert result.success
    assert character.check()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_duplicate_character(campaign):
    npc.commands.create_simple('testmann', 'human')
    result = npc.commands.create_simple('testmann', 'human')
    assert not result.success
    assert result.errcode == 1

def test_adds_group_tags(campaign):
    npc.commands.create_simple('testmann', 'human', groups=['fork', 'spoon'])
    data = campaign.get_character_data('testmann.nwod')
    assert data['group'] == ['fork', 'spoon']

def test_adds_foreign_tag(campaign):
    """With just --foreign, add the tag and no notes"""
    npc.commands.create_simple('testmann', 'human', foreign="Lives on the moon, with Steve")
    data = campaign.get_character_data('testmann.nwod')
    assert data['foreign'] == ['Lives on the moon, with Steve']

class TestDead:
    """Test permutations of the --dead arg"""

    def test_no_dead_tag(self, campaign):
        """Characters shouldn't be dead without the command"""
        npc.commands.create_simple('testmann', 'human')
        data = campaign.get_character_data('testmann.nwod')
        assert 'dead' not in data

    def test_bare_dead_tag(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_simple('testmann', 'human', dead='')
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['']

    def test_dead_tag_with_notes(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_simple('testmann', 'human', dead='Died in a tragic toast accident')
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['Died in a tragic toast accident']
