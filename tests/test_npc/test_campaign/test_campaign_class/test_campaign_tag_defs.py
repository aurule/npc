from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_includes_global_tags(tmp_campaign):
    tag_defs = tmp_campaign.campaign_tag_defs

    assert "type" in tag_defs

def test_includes_system_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    tag_defs = tmp_campaign.campaign_tag_defs

    assert "concept" in tag_defs

def test_includes_campaign_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "tags": {
            "test": {
                "desc": "Marks as test"
            }
        }
    })
    tag_defs = tmp_campaign.campaign_tag_defs

    assert "test" in tag_defs
