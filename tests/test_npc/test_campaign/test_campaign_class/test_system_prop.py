from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_creates_correct_object(tmp_campaign):
    system = tmp_campaign.system

    assert system.name == tmp_campaign.settings.get(f"npc.systems.{tmp_campaign.system_key}.name")
