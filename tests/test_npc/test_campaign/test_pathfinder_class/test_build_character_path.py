import pytest

from tests.fixtures import tmp_campaign, create_character
from npc.campaign import Campaign
from npc.db import DB

from npc.campaign import Pathfinder

def set_subpath_components(campaign, *components):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "first_value",
                    "tags": components
                }
            ]
        }
    }
    campaign.patch_campaign_settings(patch)

class TestWithExistingDirsOnly:
    def test_tag_value_exists_adds_tag(self, tmp_campaign):
        set_subpath_components(tmp_campaign, "test")
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=True)

        assert result == tmp_campaign.characters_dir / "blep"

    def test_tag_value_no_exists_skips(self, tmp_campaign):
        set_subpath_components(tmp_campaign, "test")
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=True)

        assert result == tmp_campaign.characters_dir

    def test_missing_first_component_adds_second(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["brains"]
                    },
                    {
                        "selector": "first_value",
                        "tags": ["test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=True)

        assert result == tmp_campaign.characters_dir / "blep"

    def test_first_component_not_exist_adds_second(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["brains"]
                    },
                    {
                        "selector": "first_value",
                        "tags": ["test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        tmp_campaign.characters_dir.joinpath("blep").mkdir()
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep"), ("brains", "sure")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=True)

        assert result == tmp_campaign.characters_dir / "blep"

class TestWithNonExistingDirs:
    def test_has_tag_adds_tag(self, tmp_campaign):
        set_subpath_components(tmp_campaign, "test")
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir / "blep"

    def test_no_tag_skips(self, tmp_campaign):
        set_subpath_components(tmp_campaign, "test")
        db = DB(clearSingleton=True)
        character = create_character([("nah", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir

class TestWithBadSelector:
    def test_throws_error(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "nopealope",
                        "tags": ["brains", "test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB(clearSingleton=True)
        character = create_character([("nah", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        with pytest.raises(ValueError):
            finder.build_character_path(character)
