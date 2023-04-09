from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import parse_yaml

def test_true_with_campaign(tmp_campaign):
    (tmp_path, settings) = tmp_campaign

    assert settings.has_campaign

def test_false_without_campaign():
    settings = Settings()

    assert not settings.has_campaign
