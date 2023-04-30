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

def test_adds_shallow_nested_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    tags = [
        RawTag("group", "Testers"),
        RawTag("rank", "Lead"),
    ]

    character = factory.make("Test Mann", tags=tags)

    assert character.tags[0].subtags[0].value == "Lead"