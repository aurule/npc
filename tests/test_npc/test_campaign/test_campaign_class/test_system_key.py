from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_returns_saved_description(tmp_campaign):
    assert tmp_campaign.system_key == tmp_campaign.settings.get("campaign.system")
