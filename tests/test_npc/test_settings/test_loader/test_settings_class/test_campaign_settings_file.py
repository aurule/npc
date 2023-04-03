from tests.fixtures import fixture_file
from npc.campaign import init

from npc.settings import Settings
from npc.util import parse_yaml

def test_gets_the_file(tmp_path):
    settings = init(tmp_path, name="Test Campaign", system="generic")

    assert settings.campaign_settings_file == tmp_path / ".npc" / "settings.yaml"

def test_aborts_on_no_campaign():
    settings = Settings()

    assert settings.campaign_settings_file is None
