from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_returns_saved_name(tmp_campaign):
    assert tmp_campaign.name == tmp_campaign.settings.get("campaign.name")
