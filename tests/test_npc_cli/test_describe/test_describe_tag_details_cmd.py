import yaml
from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

class TestWithoutCampaign():
    def test_requires_system(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tag", "--tag", "type"])

        assert "--system option must be provided" in result.output

    def test_shows_system_tag(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tag", "--system", "fate", "--tag", "aspect"])

        assert "aspect" in result.output

class TestInCampaign():
    def test_shows_campaign_system_tag(self, tmp_campaign):
        runner = CliRunner()

        tmp_campaign.patch_campaign_settings({"system": "fate"})

        with runner.isolated_filesystem(tmp_campaign.root):
            result = runner.invoke(cli, ["describe", "tag", "--tag", "aspect"])

            assert "aspect" in result.output

    def test_shows_campaign_specific_tag(self, tmp_campaign):
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
            result = runner.invoke(cli, ["describe", "tag", "--tag", "test"])

            assert "test" in result.output

class TestForSingleType():
    def test_shows_type_tag(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tag", "--system", "nwod", "--type", "changeling", "--tag", "seeming"])

        assert "seeming" in result.output

    def test_requires_type_to_exist(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "tag", "--system", "nwod", "--type", "nope", "--tag", "seeming"])

        assert "'nope' is not one of" in result.output

class TestSubtag():
    def test_requires_context(self):
        pass

    def test_shows_subtag(self):
        pass
