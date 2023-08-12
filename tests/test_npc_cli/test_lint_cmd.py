from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated, clean_db

from npc_cli import cli

@isolated
@clean_db
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, "lint")

    assert "Not a campaign" in result.output

@isolated
@clean_db
def test_shows_bad_characters(tmp_campaign, runner):
    runner.invoke(cli, "new person -n 'Test Mann' -m tester")

    result = runner.invoke(cli, "lint")

    assert "Test Mann" in result.output
    assert "missing description" in result.output
