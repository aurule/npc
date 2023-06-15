from tests.fixtures import tmp_campaign
from npc.characters import CharacterFactory, Character, RawTag
from npc.campaign import Campaign
from npc.db import DB

from npc.characters import CharacterWriter

def create_character(tags: list, tmp_campaign: Campaign, db: DB, type_key="person", **kwargs) -> Character:
    factory = CharacterFactory(tmp_campaign)
    rawtags = [RawTag(*tag) for tag in tags]

    character = factory.make("Test Mann", tags=rawtags, type_key=type_key, **kwargs)
    with db.session() as session:
        session.add(character)
        session.commit()
        character.tags # load the tags immediately to prevent DetachedInstanceError later
    return character

def test_creates_missing_file(tmp_campaign):
    db = DB(clearSingleton=True)
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    assert loc.exists()

def test_overwrites_existing_file(tmp_campaign):
    db = DB(clearSingleton=True)
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    loc.touch()
    character = create_character([], tmp_campaign, db, path=loc, body="contents!")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "contents!" in contents

def test_writes_attr_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "@type person" in contents

def test_writes_real_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([("race", "elf")], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "@race elf" in contents

def test_writes_body(tmp_campaign):
    db = DB(clearSingleton=True)
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="contents!")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "contents!" in contents
