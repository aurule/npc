from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

def test_aborts_on_missing_campaign(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ['report', '-r', 'values', '-t', 'type'])

        assert "Not a campaign" in result.output

def test_shows_values_breakdown(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        runner.invoke(cli, ['new', 'person', '-n', 'test', '-m', 'tester'])
        runner.invoke(cli, ['new', 'person', '-n', 'testy', '-m', 'tester'])
        result = runner.invoke(cli, ['report', '-r', 'values', '-t', 'type'])

        assert "person" in result.output
