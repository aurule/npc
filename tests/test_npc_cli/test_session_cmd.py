from pathlib import Path
from click.testing import CliRunner

from npc_cli import cli

class TestCampaignLocation():
    def test_aborts_on_missing_campaign(self, tmp_path):
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ['session'])

            assert "Not a campaign" in result.output
