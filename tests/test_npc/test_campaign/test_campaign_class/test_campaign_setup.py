from tests.fixtures import fixture_file

from npc.campaign import Campaign
from npc.settings import Settings

def test_saves_campaign_root():
    campaign = Campaign(fixture_file(["campaigns", "simple"]))

    assert campaign.root == fixture_file(["campaigns", "simple"])

def test_creates_settings_if_missing():
    campaign = Campaign(fixture_file(["campaigns", "simple"]))

    assert isinstance(campaign.settings, Settings)

def test_loads_campaign_settings():
    campaign = Campaign(fixture_file(["campaigns", "simple"]))

    assert "name" in campaign.settings.get("campaign")

def test_loads_campaign_systems():
    campaign = Campaign(fixture_file(["campaigns", "large"]))

    assert "custom" in campaign.settings.get("npc.systems").keys()
