from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_gets_correct_key(tmp_campaign):
    assert tmp_campaign.system_key == tmp_campaign.settings.get("campaign.system")

def test_gets_generic_key_when_not_defined(tmp_path):
    campaign = Campaign(tmp_path)

    assert campaign.system_key == "generic"
