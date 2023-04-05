from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import parse_yaml

def test_gets_the_file(tmp_campaign):
    (tmp_path, settings) = tmp_campaign

    assert settings.campaign_settings_file == tmp_path / ".npc" / "settings.yaml"

def test_aborts_on_no_campaign():
    settings = Settings()

    assert settings.campaign_settings_file is None
