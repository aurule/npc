from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

def test_aborts_on_missing_campaign(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ['new', "person", "-n", "test", "-m", "test"])

        assert "Not a campaign" in result.output

def test_aborts_on_bad_type(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        result = runner.invoke(cli, ['new', "nope", "-n", "test", "-m", "test"])

        assert "'nope' is not one of 'person'" in result.output

def test_makes_character_file(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        result = runner.invoke(cli, ['new', "person", "-n", "test", "-m", "test"])

        assert tmp_campaign.characters_dir.joinpath("test - test.npc").exists()
