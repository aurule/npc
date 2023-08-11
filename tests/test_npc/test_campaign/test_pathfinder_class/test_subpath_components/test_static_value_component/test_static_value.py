import pytest

from tests.fixtures import tmp_campaign, create_character, db
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag

from npc.campaign.subpath_components import StaticValueComponent

def test_returns_value_with_existing(tmp_campaign, db):
    spec = {
        "selector": "static_value",
        "value": "blep"
    }
    tmp_campaign.characters_dir.joinpath("blep").mkdir()
    character = create_character([], tmp_campaign, db)
    comp = StaticValueComponent(db, spec, True)

    result = comp.value(character, tmp_campaign.characters_dir)

    assert result == "blep"

def test_returns_value_with_non_existing(tmp_campaign, db):
    spec = {
        "selector": "static_value",
        "value": "blep"
    }
    tmp_campaign.characters_dir.joinpath("blep").mkdir()
    character = create_character([], tmp_campaign, db)
    comp = StaticValueComponent(db, spec, False)

    result = comp.value(character, tmp_campaign.characters_dir)

    assert result == "blep"
