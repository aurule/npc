from tests.fixtures import tmp_campaign

from npc.characters import CharacterFactory

def test_saves_name(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann")

    assert character.name == "Test Mann"

def test_saves_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "person")

    assert character.type_key == "person"

def test_allows_unknown_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "nope")

    assert character.type_key == "nope"
