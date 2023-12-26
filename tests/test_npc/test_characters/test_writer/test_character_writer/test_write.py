from tests.fixtures import tmp_campaign, create_character, db

from npc.campaign import Campaign

from npc.characters import CharacterWriter

def test_creates_missing_file(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    assert loc.exists()

def test_overwrites_existing_file(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    loc.touch()
    character = create_character([], tmp_campaign, db, path=loc, body="contents!")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "contents!" in contents

def test_writes_attr_tags(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "@type person" in contents

def test_writes_real_tags(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([("race", "elf")], tmp_campaign, db, path=loc, body="")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "@race elf" in contents

def test_writes_body(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann.npc"
    character = create_character([], tmp_campaign, db, path=loc, body="contents!")
    writer = CharacterWriter(tmp_campaign, db=db)

    writer.write(character)

    with loc.open() as f:
        contents = f.read()
    assert "contents!" in contents
