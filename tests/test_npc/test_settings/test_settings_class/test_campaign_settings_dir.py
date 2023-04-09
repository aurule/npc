from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import parse_yaml

def test_gets_the_file(tmp_campaign):
    root = tmp_campaign.root
    settings = tmp_campaign.settings

    assert settings.campaign_settings_dir == root / ".npc"

def test_aborts_on_no_campaign():
    settings = Settings()

    assert settings.campaign_settings_dir is None
