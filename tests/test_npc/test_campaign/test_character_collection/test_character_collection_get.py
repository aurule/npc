from tests.fixtures import tmp_campaign, db
from sqlalchemy import select
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_retrieves_existing_record(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)
    character_id = collection.create(realname="Fido", type_key="person")

    result = collection.get(character_id)

    assert result.realname == "Fido"

def test_returns_none_for_missing_record(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)

    result = collection.get(555)

    assert result is None
