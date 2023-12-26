from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated, clean_db

import shutil

from npc_cli import cli

@isolated
@clean_db
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, "reorg")

    assert "Not a campaign" in result.output

@isolated
@clean_db
def test_shows_conflicts(tmp_campaign, runner):
    runner.invoke(cli, "new person -n 'Test Mann' -m tester")
    char_file = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    extra_dir = tmp_campaign.characters_dir / "extra"
    shutil.move(char_file, extra_dir)
    runner.invoke(cli, "new person -n 'Test Mann' -m tester")

    result = runner.invoke(cli, "reorg")

    assert "Found these problems" in result.output

@isolated
@clean_db
def test_ends_when_nothing_to_do(tmp_campaign, runner):
    result = runner.invoke(cli, "reorg")

    assert "Nothing needs to be moved" in result.output
