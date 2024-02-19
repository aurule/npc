import yaml

from npc_gui.util import RecentCampaigns

def test_loads_existing_data(tmp_path):
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

    assert recents.get("campaigns")[0]["name"] == "Test Campaign"
