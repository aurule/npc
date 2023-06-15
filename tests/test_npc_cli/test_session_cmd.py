from pathlib import Path
from click.testing import CliRunner
from tests.fixtures import runner, isolated

from npc_cli import cli

class TestCampaignLocation():
    @isolated
    def test_aborts_on_missing_campaign(self, tmp_path, runner):
        result = runner.invoke(cli, ['session'])

        assert "Not a campaign" in result.output
