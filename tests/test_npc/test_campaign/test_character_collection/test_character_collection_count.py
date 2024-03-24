from tests.fixtures import tmp_campaign, db

from npc.campaign import CharacterCollection

def test_gets_stored_count(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)
    collection.create(realname="Fido", type_key="person")

    assert collection.count == 1

def test_caches_value(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.count = 5

    assert tmp_campaign.stats.get(CharacterCollection.CACHE_KEY) == 5
