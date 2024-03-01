import pytest
from tests.fixtures import tmp_campaign, db
from npc.util.errors import NotFoundError

from npc.campaign import CharacterCollection

def test_changes_existing_record(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)
    char_id = collection.create(realname="Test Mann", type_key="person")

    collection.update(char_id, realname="Fake Mann")

    record = collection.get(char_id)
    assert record.realname == "Fake Mann"

def test_errors_on_bad_id(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)

    with pytest.raises(NotFoundError):
        collection.update(555, realname="ohno")

def test_errors_on_bad_attr(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)
    char_id = collection.create(realname="Test Mann", type_key="person")

    with pytest.raises(AttributeError):
        collection.update(char_id, fuzzbutt="so fluffy")
