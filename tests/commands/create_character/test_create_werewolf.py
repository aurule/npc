import npc
import pytest
import os
import re

def test_creates_character(campaign):
    result = npc.commands.create_character.werewolf('werewolf mann', 'cahalith')
    character = campaign.get_character('werewolf mann.nwod')
    assert result.success
    assert character.exists()
    assert campaign.get_absolute(result.openable[0]) == str(character)

def test_adds_group_tags(campaign):
    result = npc.commands.create_character.werewolf('werewolf mann', 'cahalith', groups=['fork', 'spoon'])
    data = campaign.get_character_data('werewolf mann.nwod')
    assert data['group'] == ['fork', 'spoon']

def test_duplicate_character(campaign):
    npc.commands.create_character.werewolf('werewolf mann', 'cahalith')
    result = npc.commands.create_character.werewolf('werewolf mann', 'cahalith')
    assert not result.success

def test_adds_auspice(campaign):
    npc.commands.create_character.werewolf('werewolf mann', 'cahalith')
    data = campaign.get_character_data('werewolf mann.nwod')
    assert 'Cahalith' in data['auspice']

def test_adds_tribe(campaign):
    npc.commands.create_character.werewolf('werewolf mann', 'cahalith', tribe='Bone Talons')
    data = campaign.get_character_data('werewolf mann.nwod')
    assert 'Bone Talons' in data['tribe']

def test_adds_pack(campaign):
    npc.commands.create_character.werewolf('werewolf mann', 'cahalith', pack='Foobars')
    data = campaign.get_character_data('werewolf mann.nwod')
    assert 'Foobars' in data['pack']
