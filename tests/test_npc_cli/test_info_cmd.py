from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

def test_aborts_on_missing_campaign(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ['info'])

        assert "Not a campaign" in result.output

def test_shows_campaign_name(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        result = runner.invoke(cli, ['info'])

        assert tmp_campaign.name in result.output
