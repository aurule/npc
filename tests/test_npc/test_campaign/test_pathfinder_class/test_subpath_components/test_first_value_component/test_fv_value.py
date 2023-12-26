import pytest

from tests.fixtures import tmp_campaign, create_character, db
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag

from npc.campaign.subpath_components import FirstValueComponent

class TestWithExistingDirs:
    def test_tag_value_exists_returns_tag(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_tag_value_no_exists_returns_none(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

    def test_tag_values_both_exist_returns_first(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        tmp_campaign.characters_dir.joinpath("aleph").mkdir()
        character = create_character([
            ("test", "blep"),
            ("test", "aleph"),
        ], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_no_tag_returns_none(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        character = create_character([("nah", "blep")], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

    def test_has_second_tag_returns_second(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"]
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        tmp_campaign.characters_dir.joinpath("beep").mkdir()
        character = create_character([
            ("nah", "beep"),
            ("test", "blep"),
        ], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_both_tags_exist_returns_first(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"]
        }
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        tmp_campaign.characters_dir.joinpath("aleph").mkdir()
        character = create_character([
            ("brains", "blep"),
            ("test", "aleph"),
        ], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

class TestWithNonExistingDirs:
    def test_has_tag_returns_tag(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        character = create_character([("test", "blep")], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_has_tag_returns_first_value(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        character = create_character([
            ("test", "blep"),
            ("test", "boop"),
        ], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"

    def test_no_tag_returns_none(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        character = create_character([("nah", "blep")], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

    def test_has_second_tag_returns_second(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["test"]
        }
        character = create_character([
                ("nah", "beep"),
                ("test", "blep")
            ], tmp_campaign, db)
        comp = FirstValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "blep"
