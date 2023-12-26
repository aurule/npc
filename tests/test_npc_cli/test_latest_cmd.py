from pathlib import Path
from click.testing import CliRunner
from tests.fixtures import runner, isolated, clean_db

from npc_cli import cli

class TestCampaignLocation():
    @isolated
    @clean_db
    def test_aborts_on_missing_campaign(self, tmp_path, runner):
        result = runner.invoke(cli, 'latest')

        assert "Not a campaign" in result.output
