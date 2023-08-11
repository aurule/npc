from tests.fixtures import tmp_campaign, db

from npc.campaign import CharacterCollection

def test_includes_npc_suffix(tmp_campaign, db):
    collection = CharacterCollection(tmp_campaign, db=db)

    assert ".npc" in collection.allowed_suffixes

def test_includes_type_suffix(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
    collection = CharacterCollection(tmp_campaign, db=db)

    assert ".nwod" in collection.allowed_suffixes
