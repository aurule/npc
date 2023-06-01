from tests.fixtures import tmp_campaign
from sqlalchemy import select
from npc.db import DB
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_makes_character_object(tmp_campaign):
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    character_id = collection.create(realname="Fido", type_key="person")

    with db.session() as session:
        query = select(Character).where(Character.id == 1)
        result = session.scalars(query).first()
        assert result.name == "Fido"

def test_puts_character_in_db(tmp_campaign):
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    character_id = collection.create(realname="Fido", type_key="person")

    assert character_id == 1
