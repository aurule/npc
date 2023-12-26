from tests.fixtures import tmp_campaign
from npc.campaign import init

from npc.util import parse_yaml

def test_updates_settings_obj(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"name": "New Name"})

    assert tmp_campaign.name == "New Name"

def test_updates_saved_settings(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"name": "New Name"})

    refreshed = parse_yaml(tmp_campaign.settings_file)
    assert refreshed["campaign"]["name"] == "New Name"
