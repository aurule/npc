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
    assert data['group'] == ['fork', 'spoon']

def test_duplicate_character(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    result = npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    assert not result.success

def test_adds_seeming(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Beast' in data['seeming']

def test_adds_seeming_notes(campaign):
    """Seeming notes should be added within the character file.

    This test does not ensure that the notes are correct."""

    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    character = campaign.get_character('changeling mann.nwod')
    assert '    Seeming Beast (8-again animal ken and free specialty; glamour adds to presence and composure; -4 untrained mental; no 10-again on Int)' in character.read_text()

def test_adds_kith(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Hunterheart' in data['kith']

def test_adds_kith_notes(campaign):
    """Kith notes should be added within the character file.

    This test does not ensure that the notes are correct."""

    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart')
    character = campaign.get_character('changeling mann.nwod')
    assert '    Kith    Hunterheart (Unarmed attacks deal lethal damage)' in character.read_text()

def test_adds_court(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', court='Summer')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Summer' in data['court']

def test_adds_motley(campaign):
    npc.commands.create_character.changeling('changeling mann', 'Beast', 'Hunterheart', motley='Funny Bones Men')
    data = campaign.get_character_data('changeling mann.nwod')
    assert 'Funny Bones Men' in data['motley']
