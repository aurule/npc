from tests.fixtures import tmp_campaign, create_character, db

from npc.campaign.subpath_components import MatchValueComponent

class TestWithOnlyExisting():
    def test_matching_tag_returns_value_with_dir(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"],
            "equals": "testing",
            "value": "Test Me",
        }
        tmp_campaign.characters_dir.joinpath("Test Me").mkdir()
        character = create_character([("test", "testing")], tmp_campaign, db)
        comp = MatchValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "Test Me"

    def test_matching_tag_returns_none_without_dir(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"],
            "equals": "testing",
            "value": "Test Me",
        }
        character = create_character([("test", "testing")], tmp_campaign, db)
        comp = MatchValueComponent(db, spec, True)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None

class TestWithoutOnlyExisting():
    def test_matching_tag_returns_value(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"],
            "equals": "testing",
            "value": "Test Me",
        }
        character = create_character([("test", "testing")], tmp_campaign, db)
        comp = MatchValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result == "Test Me"

    def test_no_matching_tag_returns_none(self, tmp_campaign, db):
        spec = {
            "selector": "first_value",
            "tags": ["brains", "test"],
            "equals": "testing",
            "value": "Test Me",
        }
        character = create_character([("test", "nope")], tmp_campaign, db)
        comp = MatchValueComponent(db, spec, False)

        result = comp.value(character, tmp_campaign.characters_dir)

        assert result is None
