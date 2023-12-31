import pytest

from tests.fixtures import tmp_campaign, create_character, db
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag

from npc.campaign.subpath_components import StaticValueComponent

class TestWithOnlyExisting():
    def test_returns_value_with_existing(self, tmp_campaign, db):
        spec = {
            "selector": "static_value",
            "value": "blep"
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        character = create_character([], tmp_campaign, db)
        comp = StaticValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_returns_none_with_non_existing(self, tmp_campaign, db):
        spec = {
            "selector": "static_value",
            "value": "blep"
        }
        character = create_character([], tmp_campaign, db)
        comp = StaticValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

class TestWithoutOnlyExisting():
    def test_returns_value_with_existing(self, tmp_campaign, db):
        spec = {
            "selector": "static_value",
            "value": "blep"
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        character = create_character([], tmp_campaign, db)
        comp = StaticValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_returns_value_with_non_existing(self, tmp_campaign, db):
        spec = {
            "selector": "static_value",
            "value": "blep"
        }
        character = create_character([], tmp_campaign, db)
        comp = StaticValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"
