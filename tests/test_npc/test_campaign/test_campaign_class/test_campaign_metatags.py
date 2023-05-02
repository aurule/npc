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
    metatags = tmp_campaign.metatags

    assert "brewer" in metatags

def test_includes_system_metatags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
    metatags = tmp_campaign.metatags

    assert "changeling" in metatags

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
    metatags = tmp_campaign.metatags

    assert "brewer" in metatags
