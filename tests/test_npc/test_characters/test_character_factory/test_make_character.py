from tests.fixtures import tmp_campaign
from npc.characters import RawTag

from npc.characters import CharacterFactory

def test_saves_realname(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann")

    assert character.realname == "Test Mann"

def test_saves_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "person")

    assert character.type_key == "person"

def test_allows_unknown_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "nope")

    assert character.type_key == "nope"

def test_handles_mapped_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    tags = [RawTag("type", "humanoid")]

    character = factory.make("Test Mann", tags=tags)

    assert character.type_key == "humanoid"

def test_adds_regular_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    tags = [RawTag("kingdom", "animalia")]

    character = factory.make("Test Mann", tags=tags)

    assert "kingdom" in [tag.name for tag in character.tags]

class TestNestedTag():
    def test_adds_deep_nested_tags(self, tmp_campaign):
        new_defs = {
            "tags": {
                "test1": {
                    "desc": "First test tag",
                    "subtags": {
                        "test2": {
                            "desc": "Second test tag",
                            "subtags": {
                                "test3": {
                                    "desc": "Third test tag",
                                }
                            }
                        }
                    }
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test1", "Testers"),
            RawTag("test2", "Lead"),
            RawTag("test3", "Pro"),
        ]

        print(tmp_campaign.get_tag("test2"))

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].subtags[0].value == "Pro"

    def test_adds_shallow_nested_tags(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("group", "Testers"),
            RawTag("rank", "Lead"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].value == "Lead"
