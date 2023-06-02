from sqlalchemy import select, func
from tests.fixtures import tmp_campaign
from npc.db import DB
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_loads_npc_sheets(tmp_campaign):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        query = select(Character).where(Character.id == 1)
        result = session.scalars(query).first()
        assert result.name == "Test Mann"

def test_loads_type_sheets(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    loc = tmp_campaign.characters_dir / "Test Mann - tester.fate"
    with loc.open('w', newline="\n") as file:
        file.write("@type supporting")
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        query = select(Character).where(Character.id == 1)
        result = session.scalars(query).first()
        assert result.name == "Test Mann"

def test_loads_from_subdirs(tmp_campaign):
    subdir = tmp_campaign.characters_dir / "yasplz"
    subdir.mkdir()
    loc = subdir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        query = select(Character).where(Character.id == 1)
        result = session.scalars(query).first()
        assert result.name == "Test Mann"

def test_skips_from_ignore_dirs(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "characters": {
            "ignore_subpaths": ["noplz"]
        }
    })
    ignored = tmp_campaign.characters_dir / "noplz"
    ignored.mkdir()
    loc = ignored / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        query = func.count(Character.id)
        result = session.scalars(query).first()
        assert result == 0

def test_skips_non_sheets(tmp_campaign):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.nope"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        query = func.count(Character.id)
        result = session.scalars(query).first()
        assert result == 0
