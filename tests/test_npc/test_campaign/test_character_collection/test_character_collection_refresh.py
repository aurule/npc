from tests.fixtures import tmp_campaign, db
from npc.characters import CharacterReader
from npc.db import character_repository

from npc.campaign import CharacterCollection

def test_loads_new_files(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.refresh()

    with db.session() as session:
        result = session.execute(character_repository.all()).all()
        assert len(result) == 1

def test_skips_older_files(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)
    reader = CharacterReader(loc)
    old_id = collection.create(
        realname = reader.name(),
        mnemonic = reader.mnemonic(),
        body = reader.body(),
        tags = reader.tags(),
        path = reader.character_path,
    )

    collection.refresh()

    with db.session() as session:
        result = session.execute(character_repository.all()).scalar()
        assert(result.id) == old_id

def test_deletes_record_without_file(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)
    character_id = collection.create(realname="Fido", type_key="person")

    collection.refresh()

    with db.session() as session:
        result = session.execute(character_repository.all()).all()
        assert len(result) == 0

def test_replaces_record_with_updated_file(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)
    reader = CharacterReader(loc)
    old_id = collection.create(
        realname = reader.name(),
        mnemonic = reader.mnemonic(),
        body = reader.body(),
        tags = reader.tags(),
        path = reader.character_path,
    )
    collection.update(old_id, file_mtime = loc.stat().st_mtime - 10)
    with loc.open('a', newline="\n") as file:
        file.write("\n@delist")

    collection.refresh()

    with db.session() as session:
        result = session.execute(character_repository.all()).scalar()
        assert result.delist == True
