from tests.fixtures import tmp_campaign
from npc.characters import CharacterFactory, Character, RawTag
from npc.campaign import Campaign
from npc.db import DB

from npc.characters import CharacterWriter

def create_character(tags: list, tmp_campaign: Campaign, db: DB) -> Character:
    factory = CharacterFactory(tmp_campaign)
    rawtags = [RawTag(*tag) for tag in tags]

    character = factory.make("Test Mann", type_key="person", tags=rawtags)
    with db.session() as session:
        session.add(character)
        session.commit()
        character.tags # load the tags immediately to prevent DetachedInstanceError later
    return character

def test_includes_desc(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = factory.make("Test Mann", type_key="person", desc="test description")
    db = DB(clearSingleton=True)
    with db.session() as session:
        session.add(character)
        session.commit()
        character.tags # load the tags immediately to prevent DetachedInstanceError later
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.make_contents(character)

    assert "test description" in result

def test_includes_contags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("delist", True)], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.make_contents(character)

    assert "@delist" in result

def test_includes_normal_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("title", "True Bro")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.make_contents(character)

    assert "@title True Bro" in result

def test_includes_all_normal_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([
        ("title", "True Bro"),
        ("title", "Esteemed"),
    ], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.make_contents(character)

    assert "@title True Bro" in result
    assert "@title Esteemed" in result

def test_includes_unknown_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.make_contents(character)

    assert "@asdf literally what" in result
