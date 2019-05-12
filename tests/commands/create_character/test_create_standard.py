import npc
import pytest
import os

def test_missing_template(campaign):
    result = npc.commands.create_character.standard('noname', 'notfound')
    assert not result.success
    assert result.errcode == 1

@pytest.mark.parametrize('chartype', ['human', 'fetch', 'goblin', 'spirit'])
def test_creates_character(campaign, chartype):
    result = npc.commands.create_character.standard('testmann', chartype)
    character = campaign.get_character('testmann.nwod')
    assert result.success
    assert character.exists()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_duplicate_character(campaign):
    npc.commands.create_character.standard('testmann', 'human')
    result = npc.commands.create_character.standard('testmann', 'human')
    assert not result.success
    assert result.errcode == 1

def test_adds_group_tags(campaign):
    npc.commands.create_character.standard('testmann', 'human', groups=['fork', 'spoon'])
    data = campaign.get_character_data('testmann.nwod')
    assert data['group'] == ['fork', 'spoon']

def test_adds_filled_foreign_tag(campaign):
    """With just --foreign, add the tag with notes"""
    npc.commands.create_character.standard('testmann', 'human', foreign="Lives on the moon, with Steve")
    data = campaign.get_character_data('testmann.nwod')
    assert data['foreign'] == ['Lives on the moon, with Steve']

def test_adds_location_tag(campaign):
    npc.commands.create_character.standard('testmann', 'human', location="Sea of Tranquility")
    data = campaign.get_character_data('testmann.nwod')
    assert data['location'] == ['Sea of Tranquility']

class TestDefaults:
    def test_adds_default_values(self, campaign, prefs):
        prefs.update_key('tag_defaults.title', 'The Chill')
        npc.commands.create_character.standard('testmann', 'human', prefs=prefs)
        data = campaign.get_character_data('testmann.nwod')
        assert data['title'] == ['The Chill']

    def test_adds_user_values(self, campaign, prefs):
        prefs.update_key('tag_defaults.location', 'The Moon')
        npc.commands.create_character.standard('testmann', 'human', location="The Earth", prefs=prefs)
        data = campaign.get_character_data('testmann.nwod')
        assert data['location'] == ['The Earth']

class TestDead:
    """Test permutations of the --dead arg"""

    def test_no_dead_tag(self, campaign):
        """Characters shouldn't be dead without the command"""
        npc.commands.create_character.standard('testmann', 'human')
        data = campaign.get_character_data('testmann.nwod')
        assert 'dead' not in data

    def test_bare_dead_tag(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_character.standard('testmann', 'human', dead='')
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['']

    def test_dead_tag_with_notes(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_character.standard('testmann', 'human', dead='Died in a tragic toast accident')
        data = campaign.get_character_data('testmann.nwod')
        assert data['dead'] == ['Died in a tragic toast accident']
