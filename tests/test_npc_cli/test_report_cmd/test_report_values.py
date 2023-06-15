from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated

from npc_cli import cli

@isolated
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, 'report -r values -t type')

    assert "Not a campaign" in result.output

@isolated
def test_shows_values_breakdown(tmp_campaign, runner):
    runner.invoke(cli, 'new person -n test -m tester')
    runner.invoke(cli, 'new person -n testy -m tester')
    result = runner.invoke(cli, 'report -r values -t type')

    assert "person" in result.output
