from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated, clean_db

from npc_cli import cli

@isolated
@clean_db
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, "new person -n test -m test")

    assert "Not a campaign" in result.output

@isolated
@clean_db
def test_aborts_on_bad_type(tmp_campaign, runner):
    result = runner.invoke(cli, "new nope -n test -m test")

    assert "'nope' is not one of 'person'" in result.output

@isolated
@clean_db
def test_makes_character_file(tmp_campaign, runner):
    result = runner.invoke(cli, "new person -n test -m test")

    assert tmp_campaign.characters_dir.joinpath("test - test.npc").exists()

@isolated
@clean_db
def test_makes_character_with_tags(tmp_campaign, runner):
    result = runner.invoke(cli, "new person -n test -m test -t org Shiny")

    assert tmp_campaign.characters_dir.joinpath("test - test.npc").exists()

@isolated
@clean_db
def test_makes_character_with_subtags(tmp_campaign, runner):
    result = runner.invoke(cli, "new person -n test -m test -t org Shiny -t role Happy")

    assert tmp_campaign.characters_dir.joinpath("test - test.npc").exists()
