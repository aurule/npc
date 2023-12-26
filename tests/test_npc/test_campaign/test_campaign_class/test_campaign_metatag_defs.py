from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_includes_global_metatags(tmp_campaign):
    tmp_campaign.settings.data["npc"]["metatags"] = {
        "brewer": {
            "desc": "Brewer at brainz beer",
            "set": {
                "employer": "Brainz"
            },
            "match": [
                "job"
            ]
        }
    }
    metatag_defs = tmp_campaign.campaign_metatag_defs

    assert "brewer" in metatag_defs

def test_includes_system_metatags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
    metatag_defs = tmp_campaign.campaign_metatag_defs

    assert "changeling" in metatag_defs

def test_includes_campaign_metatags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({
        "metatags": {
            "brewer": {
                "desc": "Brewer at brainz beer",
                "set": {
                    "employer": "Brainz"
                },
                "match": [
                    "job"
                ]
            }
        }
    })
    metatag_defs = tmp_campaign.campaign_metatag_defs

    assert "brewer" in metatag_defs
