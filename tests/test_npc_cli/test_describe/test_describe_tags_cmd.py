import yaml
from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

class TestWithoutCampaign():
    def test_requires_system(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tags"])

        assert "'--system' option must be provided" in result.output

    def test_shows_system_tags(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tags", "--system", "fate"])

        assert "aspect" in result.output

class TestInCampaign():
    def test_shows_campaign_system_tags(self, tmp_campaign):
        runner = CliRunner()

        tmp_campaign.patch_campaign_settings({"system": "fate"})

        with runner.isolated_filesystem(tmp_campaign.root):
            result = runner.invoke(cli, ["describe", "tags"])

            assert "aspect" in result.output

    def test_shows_campaign_specific_tags(self, tmp_campaign):
        runner = CliRunner()

        tmp_campaign.patch_campaign_settings(
            {
                "tags": {
                    "test": {
                        "name": "test",
                        "desc": "Marks for testing"
                    }
                }
            }
        )

        with runner.isolated_filesystem(tmp_campaign.root):
            result = runner.invoke(cli, ["describe", "tags"])

            assert "test" in result.output

class TestForSingleType():
    def test_shows_type_tags(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tags", "--system", "nwod", "--type", "changeling"])

        assert "seeming" in result.output

    def test_requires_type_to_exist(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tags", "--system", "nwod", "--type", "nope"])

        assert "'nope' is not one of" in result.output
