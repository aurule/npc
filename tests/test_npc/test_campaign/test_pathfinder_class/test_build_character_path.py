import pytest

from tests.fixtures import tmp_campaign
from npc.campaign import Campaign
from npc.characters import Character, Tag, CharacterFactory, RawTag
from npc.db import DB

from npc.campaign import Pathfinder

def create_character(tags: list, tmp_campaign: Campaign, db: DB) -> Character:
    factory = CharacterFactory(tmp_campaign)
    rawtags = [RawTag(*tag) for tag in tags]

    character = factory.make("Test Mann", type_key="person", tags=rawtags)
    with db.session() as session:
        session.add(character)
        session.commit()
        character.tags # load the tags immediately to prevent DetachedInstanceError later
    return character

class TestWithExistingDirsOnly:
    pass
    # character has named tag, value exists: adds to path
    # character has named tag, value not exist: does not add
    # character has two values for named tag, values both exist: adds first value
    # character does not have named tag: does not add
    # character only has second named tag, value exists: adds to path
    # character has first and second tag, values both exist: adds first tag value

class TestWithNonExistingDirs:
    def test_has_tag_adds_tag(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB(clearSingleton=True)
        character = create_character([("test", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir / "blep"

    def test_no_tag_skips(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB(clearSingleton=True)
        character = create_character([("nah", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir

    def test_has_second_tag_adds(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["brains", "test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB(clearSingleton=True)
        character = create_character([
                ("nah", "beep"),
                ("test", "blep")
            ], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir / "blep"

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

class TestWithMissingTagsProp:
    def test_throws_error(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "xtags": ["brains", "test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB(clearSingleton=True)
        character = create_character([("nah", "blep")], tmp_campaign, db)
        finder = Pathfinder(tmp_campaign, db=db)

        with pytest.raises(KeyError):
            finder.build_character_path(character)
