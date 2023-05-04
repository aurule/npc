from tests.fixtures import tmp_campaign
from npc.settings.tags import TagSpec, UndefinedTagSpec

from npc.campaign import Campaign

def test_includes_global_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})

    tag = tmp_campaign.get_type_tag("type", "changeling")

    assert isinstance(tag, TagSpec)
    assert tag.name == "type"

def test_includes_system_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "fate"})

    tag = tmp_campaign.get_type_tag("concept", "supporting")

    assert isinstance(tag, TagSpec)
    assert tag.name == "concept"

def test_includes_campaign_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "tags": {
            "test": {
                "desc": "Marks as test"
            }
        }
    })
    tmp_campaign.patch_campaign_settings({"system": "nwod"})

    tag = tmp_campaign.get_type_tag("test", "changeling")

    assert isinstance(tag, TagSpec)
    assert tag.name == "test"

def test_gets_obj_for_unknown_tag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})

    tag = tmp_campaign.get_type_tag("invalid", "changeling")

    assert isinstance(tag, UndefinedTagSpec)
    assert tag.name == "invalid"
