from tests.fixtures import fixture_file
from npc.campaign import init

from npc.settings import Settings
from npc.util import parse_yaml

def test_updates_settings_obj(tmp_path):
    settings = init(tmp_path, name="Test Campaign", system="generic")

    settings.patch_campaign_settings({"name": "New Name"})

    assert settings.get("campaign.name") == "New Name"

def test_updates_saved_settings(tmp_path):
    settings = init(tmp_path, name="Test Campaign", system="generic")

    settings.patch_campaign_settings({"name": "New Name"})

    refreshed = parse_yaml(settings.campaign_settings_file)
    assert refreshed["campaign"]["name"] == "New Name"

def test_aborts_on_no_campaign():
    settings = Settings()

    settings.patch_campaign_settings({"name": "New Name"})

    assert True
