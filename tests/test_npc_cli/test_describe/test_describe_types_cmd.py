from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

class TestWithoutCampaign():
    def test_requires_system(self):
        pass

    def test_shows_system_types(self):
        pass

class TestInCampaign():
    def test_shows_campaign_system_types(self):
        pass

    def test_shows_campaign_specific_types(self):
        pass
