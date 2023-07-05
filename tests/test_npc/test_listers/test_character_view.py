from tests.fixtures import tmp_campaign
from npc.characters import Tag, Character, CharacterFactory, RawTag

from npc.listers.character_view import CharacterView

def test_uses_character_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person")

    view = CharacterView(character)

    assert view.type == character.type_key

def test_uses_character_desc(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", desc="A very testy boi")

    view = CharacterView(character)

    assert view.description == character.desc

def test_uses_character_realname(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person")

    view = CharacterView(character)

    assert view.realname == character.realname

def test_uses_character_mnemonic(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", mnemonic="test bro")

    view = CharacterView(character)

    assert view.mnemonic == character.mnemonic

def test_adds_attr_for_tag(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", tags=[RawTag("title", "bro")])

    view = CharacterView(character)

    assert hasattr(view, "title")

def test_reuses_attr_for_tag(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", tags=[RawTag("title", "bro"), RawTag("title", "guy")])

    view = CharacterView(character)

    assert hasattr(view, "title")
    assert len(view.title.all()) == 2

def test_default_str_value(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person")

    view = CharacterView(character)

    assert str(view) == character.realname

def test_has_tag_true_with_tag(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", tags=[RawTag("title", "bro")])

    view = CharacterView(character)

    assert view.has_tag("title")

def test_has_tag_false_without_tag(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person")

    view = CharacterView(character)

    assert not view.has_tag("title")
