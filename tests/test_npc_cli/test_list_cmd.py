from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated

from npc_cli import cli

@isolated
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, "list -o -")

    assert "Not a campaign" in result.output

@isolated
def test_shows_characters(tmp_campaign, runner):
    runner.invoke(cli, "new person -n 'Test Mann' -m tester")

    result = runner.invoke(cli, "list -o -")

    assert "Test Mann" in result.output
