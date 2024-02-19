import yaml
from tests.fixtures import MockCampaign

from npc_gui.util import RecentCampaigns

def test_adds_new_campaign_to_end(tmp_path):
    test_data = {
        "campaigns": [
            {
                "name": "Test Campaign",
                "path": str(tmp_path)
            }
        ]
    }
    test_cache = tmp_path / "test_recents.yml"
    with test_cache.open("w") as f:
        yaml.dump(test_data, f)
    recents = RecentCampaigns(test_cache)
    campaign_root = tmp_path / "campaign"
    campaign_root.mkdir()
    campaign = MockCampaign(campaign_root)
    campaign.name = "New Thing"

    recents.add(campaign)

    assert recents.campaigns()[-1]["name"] == "New Thing"

def test_moves_old_campaign_to_end(tmp_path):
    test_data = {
        "campaigns": [
            {
                "name": "Test Campaign",
                "path": str(tmp_path)
            },
            {
                "name": "Second Campaign",
                "path": str(tmp_path / "second")
            }
        ]
    }
    test_cache = tmp_path / "test_recents.yml"
    with test_cache.open("w") as f:
        yaml.dump(test_data, f)
    recents = RecentCampaigns(test_cache)
    campaign_root = tmp_path
    campaign = MockCampaign(campaign_root)
    campaign.name = "Test Campaign"

    recents.add(campaign)

    assert recents.campaigns()[-1]["name"] == "Test Campaign"
    assert len(recents.campaigns()) == 2

def test_updates_old_campaign_name(tmp_path):
    test_data = {
        "campaigns": [
            {
                "name": "Test Campaign",
                "path": str(tmp_path)
            },
            {
                "name": "Second Campaign",
                "path": str(tmp_path / "second")
            }
        ]
    }
    test_cache = tmp_path / "test_recents.yml"
    with test_cache.open("w") as f:
        yaml.dump(test_data, f)
    recents = RecentCampaigns(test_cache)
    campaign_root = tmp_path
    campaign = MockCampaign(campaign_root)
    campaign.name = "Testier Campaign"

    recents.add(campaign)

    assert recents.campaigns()[-1]["name"] == "Testier Campaign"

def test_truncates_to_max_len(tmp_path):
    test_data = {
        "campaigns": [
            {
                "name": "Test Campaign",
                "path": str(tmp_path)
            },
            {
                "name": "Second Campaign",
                "path": str(tmp_path / "second")
            },
            {
                "name": "Third Campaign",
                "path": str(tmp_path / "third")
            },
            {
                "name": "Fourth Campaign",
                "path": str(tmp_path / "fourth")
            },
            {
                "name": "Fifth Campaign",
                "path": str(tmp_path / "fifth")
            },
        ]
    }
    test_cache = tmp_path / "test_recents.yml"
    with test_cache.open("w") as f:
        yaml.dump(test_data, f)
    recents = RecentCampaigns(test_cache)
    campaign_root = tmp_path / "sixth"
    campaign_root.mkdir()
    campaign = MockCampaign(campaign_root)
    campaign.name = "Sixth Campaign"

    recents.add(campaign)

    assert len(recents.campaigns()) == RecentCampaigns.MAX_RECENTS
