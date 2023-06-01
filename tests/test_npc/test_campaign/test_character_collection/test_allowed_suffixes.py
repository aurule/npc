from tests.fixtures import tmp_campaign
from npc.db import DB

from npc.campaign import CharacterCollection

def test_includes_npc_suffix(tmp_campaign):
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    assert ".npc" in collection.allowed_suffixes

def test_includes_type_suffix(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
    db = DB(clearSingleton=True)
    collection = CharacterCollection(tmp_campaign, db=db)

    assert ".nwod" in collection.allowed_suffixes
