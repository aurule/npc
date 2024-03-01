from tests.fixtures import tmp_campaign, db
from npc.db import character_repository

from npc.campaign import CharacterCollection

def test_creates_character_records(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.seed()

    with db.session() as session:
        result = session.execute(character_repository.all()).all()
        assert len(result) == 1

def test_clears_existing_records(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)
    collection.create(realname="Other Mann", type_key="person")

    collection.seed()

    with db.session() as session:
        result = session.execute(character_repository.all()).all()
        assert len(result) == 1
