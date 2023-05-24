from tests.fixtures import tmp_campaign
from npc.settings.tags import TagSpec, UndefinedTagSpec

from npc.campaign import Campaign

def test_gets_global_tag(tmp_campaign):
    tag = tmp_campaign.get_tag("type")

    assert isinstance(tag, TagSpec)
    assert tag.name == "type"

def test_gets_system_tag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    tag = tmp_campaign.get_tag("concept")

    assert isinstance(tag, TagSpec)
    assert tag.name == "concept"

def test_gets_campaign_tag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "tags": {
            "test": {
                "desc": "Marks as test"
            }
        }
    })
    tag = tmp_campaign.get_tag("test")

    assert isinstance(tag, TagSpec)
    assert tag.name == "test"

def test_gets_obj_for_unknown_tag(tmp_campaign):
    tag = tmp_campaign.get_tag("invalid")

    assert isinstance(tag, UndefinedTagSpec)
    assert tag.name == "invalid"
