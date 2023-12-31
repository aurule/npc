import pytest

from tests.fixtures import tmp_campaign, create_character, db
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag

from npc.campaign.subpath_components import ConditionalValueComponent

class TestWithOnlyExisting():
    def test_returns_value_with_tags_and_dir(self, tmp_campaign, db):
        spec = {
            "selector": "conditional_value",
            "tags": ["test"],
            "value": "something"
        }
        tmp_campaign.characters_dir.joinpath("something").mkdir()
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = ConditionalValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "something"

    def test_returns_none_with_tags_and_no_dir(self, tmp_campaign, db):
        spec = {
            "selector": "conditional_value",
            "tags": ["test"],
            "value": "something"
        }
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = ConditionalValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

class TestWithoutOnlyExisting():
    def test_returns_value_with_tags(self, tmp_campaign, db):
        spec = {
            "selector": "conditional_value",
            "tags": ["test"],
            "value": "something"
        }
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = ConditionalValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "something"

    def test_returns_none_without_tags(self, tmp_campaign, db):
        spec = {
            "selector": "conditional_value",
            "tags": ["test"],
            "value": "something"
        }
        character = create_character([("nope", "blep")], tmp_campaign, db)
        comp = ConditionalValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None
