import npc
import pytest

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

def test_create_character_with_notes(campaign):
    result = npc.commands.create_character.standard('testmann - masterful mann', 'human')
    character = campaign.get_character('testmann - masterful mann.nwod')
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
    assert list(data.tags('group').keys()) == ['fork', 'spoon']

def test_adds_filled_foreign_tag(campaign):
    """With just --foreign, add the tag with notes"""
    npc.commands.create_character.standard('testmann', 'human', foreign="Lives on the moon, with Steve")
    data = campaign.get_character_data('testmann.nwod')
    assert data.tags['foreign'] == ['Lives on the moon, with Steve']

def test_adds_location_tag(campaign):
    npc.commands.create_character.standard('testmann', 'human', location="Sea of Tranquility")
    data = campaign.get_character_data('testmann.nwod')
    assert data.tags['location'] == ['Sea of Tranquility']

class TestDefaults:
    def test_adds_default_values(self, campaign, prefs):
        prefs.update_key('tag_defaults.title', 'The Chill')
        npc.commands.create_character.standard('testmann', 'human', prefs=prefs)
        data = campaign.get_character_data('testmann.nwod')
        assert data.tags['title'] == ['The Chill']

    def test_adds_user_values(self, campaign, prefs):
        prefs.update_key('tag_defaults.location', 'The Moon')
        npc.commands.create_character.standard('testmann', 'human', location="The Earth", prefs=prefs)
        data = campaign.get_character_data('testmann.nwod')
        assert data.tags['location'] == ['The Earth']

class TestDead:
    """Test permutations of the --dead arg"""

    def test_no_dead_tag(self, campaign):
        """Characters shouldn't be dead without the command"""
        npc.commands.create_character.standard('testmann', 'human')
        data = campaign.get_character_data('testmann.nwod')
        assert not data.tags('dead').present

    def test_bare_dead_tag(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_character.standard('testmann', 'human', dead=[''])
        data = campaign.get_character_data('testmann.nwod')
        assert data.tags('dead').present

    def test_dead_tag_with_notes(self, campaign):
        """With just --dead, add the tag and no notes"""
        npc.commands.create_character.standard('testmann', 'human', dead='Died in a tragic toast accident')
        data = campaign.get_character_data('testmann.nwod')
        assert data.tags('dead').first_value() == 'Died in a tragic toast accident'
