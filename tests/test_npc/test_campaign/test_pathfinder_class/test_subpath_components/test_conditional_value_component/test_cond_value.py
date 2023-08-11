import pytest

from tests.fixtures import tmp_campaign, create_character, db
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag

from npc.campaign.subpath_components import ConditionalValueComponent

def test_returns_value_with_tags(tmp_campaign, db):
    spec = {
        "selector": "conditional_value",
        "tags": ["test"],
        "value": "something"
    }
    tmp_campaign.characters_dir.joinpath("blep").mkdir()
    character = create_character([("test", "blep")], tmp_campaign, db)
    comp = ConditionalValueComponent(db, spec, True)

    result = comp.value(character, tmp_campaign.characters_dir)

    assert result == "something"

def test_returns_none_without_tags(tmp_campaign, db):
    spec = {
        "selector": "conditional_value",
        "tags": ["test"],
        "value": "something"
    }
    tmp_campaign.characters_dir.joinpath("blep").mkdir()
    character = create_character([("nope", "blep")], tmp_campaign, db)
    comp = ConditionalValueComponent(db, spec, True)

    result = comp.value(character, tmp_campaign.characters_dir)

    assert result is None
