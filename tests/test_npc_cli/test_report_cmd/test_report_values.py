from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated

from npc_cli import cli

@isolated
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, 'report values -t type')

    assert "Not a campaign" in result.output

@isolated
def test_shows_values_breakdown(tmp_campaign, runner):
    runner.invoke(cli, 'new person -n test -m tester')
    runner.invoke(cli, 'new person -n testy -m tester')

    result = runner.invoke(cli, 'report values -t type')

    assert "person" in result.output

@isolated
def test_shows_subtag_breakdown_in_context(tmp_campaign, runner):
    runner.invoke(cli, 'new person -n test -m tester -t org Torso -t rank Bellybutton')
    runner.invoke(cli, 'new person -n testy -m tester -t org Face -t rank Nose')
    runner.invoke(cli, 'new person -n testy -m tester -t group Face -t rank Cheek')

    result = runner.invoke(cli, 'report values -t rank -c org')

    assert "Nose" in result.output
    assert "Cheek" not in result.output

@isolated
def test_shows_subtag_breakdown_absent_context(tmp_campaign, runner):
    runner.invoke(cli, 'new person -n test -m tester -t org Torso -t rank Bellybutton')
    runner.invoke(cli, 'new person -n testfy -m tester -t group Face -t rank Nose')

    result = runner.invoke(cli, 'report values -t rank -c *')

    print(result.output)

    assert "Nose" in result.output
    assert "Bellybutton" in result.output
