from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

def test_aborts_on_missing_campaign(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["lint"])

        assert "Not a campaign" in result.output

def test_shows_bad_characters(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        runner.invoke(cli, ['new', "person", "-n", "Test Mann", "-m", "tester"])
        result = runner.invoke(cli, ["lint"])

        assert "Test Mann" in result.output
        assert "missing description" in result.output
