from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_includes_global_tags(tmp_campaign):
    tags = tmp_campaign.tags

    assert "type" in tags

def test_includes_system_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    tags = tmp_campaign.tags

    assert "concept" in tags

def test_includes_campaign_tags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "tags": {
            "test": {
                "desc": "Marks as test"
            }
        }
    })
    tags = tmp_campaign.tags

    assert "test" in tags
