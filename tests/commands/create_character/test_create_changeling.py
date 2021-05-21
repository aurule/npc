import npc
import pytest

def test_creates_character(campaign):
    result = npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    character = campaign.get_character('changeling mann.nwod')
    assert result.success
    assert character.exists()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_adds_group_tags(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', groups=['fork', 'spoon'])
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'fork' in data.tags('group')
    assert 'spoon' in data.tags('group')

def test_duplicate_character(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    result = npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    assert not result.success

class TestSeeming:
    def test_adds_seeming(self, campaign):
        npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
        data = campaign.get_character_data('changeling mann.nwod')
        assert 'Beast' in data.tags['seeming']

    def test_adds_seeming_notes(self, campaign):
        """
        Seeming notes should be added within the character file.

        This test does not ensure that the notes are correct.
        """
        npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
        character = campaign.get_character('changeling mann.nwod')
        assert '    Seeming Beast (8-again animal ken and free specialty; glamour adds to presence and composure; -4 untrained mental; no 10-again on Int)' in character.read_text()

    def test_warns_on_unknown_seeming(self, campaign, capsys):
        npc.commands.create_character.changeling('changeling mann', 'Draconic', 'Hunterheart')
        _, err = capsys.readouterr()
        data = campaign.get_character_data('changeling mann.nwod')
        assert 'Draconic' in data.tags['seeming']
        assert "Unrecognized seeming 'Draconic'" in err

class TestKith:
    def test_adds_kith(self, campaign):
        npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
        data = campaign.get_character_data('changeling mann.nwod')
        assert 'Hunterheart' in data.tags['kith']

    def test_adds_kith_notes(self, campaign):
        """
        Kith notes should be added within the character file.

        This test does not ensure that the notes are correct.
        """
        npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
        character = campaign.get_character('changeling mann.nwod')
        assert '    Kith    Hunterheart (Unarmed attacks deal lethal damage)' in character.read_text()

    def test_warns_on_unknown_seeming(self, campaign, capsys):
        npc.commands.create_character.changeling('changeling mann', 'Fairest', 'Wallaby')
        _, err = capsys.readouterr()
        data = campaign.get_character_data('changeling mann.nwod')
        assert 'Wallaby' in data.tags['kith']
        assert "Unrecognized kith 'Wallaby' for seeming 'Fairest'" in err

def test_adds_court(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', court='Summer')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Summer' in data.tags['court']

def test_adds_motley(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', motley='Funny Bones Men')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Funny Bones Men' in data.tags['motley']

def test_adds_freehold(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', freehold='Funny Bones Men')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Funny Bones Men' in data.tags['freehold']

def test_adds_entitlement(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', entitlement='Funny Bones Men')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Funny Bones Men' in data.tags['entitlement']
