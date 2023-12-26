import yaml
from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

class TestWithoutCampaign():
    def test_requires_system(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "types"])

        assert "'--system' option must be provided" in result.output

    def test_shows_system_types(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["describe", "types", "--system", "fate"])

        assert "Supporting" in result.output

class TestInCampaign():
    def test_shows_campaign_system_types(self, tmp_campaign):
        runner = CliRunner()

        with runner.isolated_filesystem(tmp_campaign.root):
            result = runner.invoke(cli, ["describe", "types"])

            assert "Person" in result.output

    def test_shows_campaign_specific_types(self, tmp_campaign):
        runner = CliRunner()

        pet_def = {
            "pet": {
                "name": "Pet",
                "desc": "A domestic animal kept for companionship"
            }
        }
        new_type_file = tmp_campaign.settings_dir.joinpath("types", "pet.yaml")
        new_type_file.parent.mkdir()
        new_type_file.touch()
        with new_type_file.open('w', newline="\n") as f:
            yaml.dump(pet_def, f)

        with runner.isolated_filesystem(tmp_campaign.root):
            result = runner.invoke(cli, ["describe", "types"])

            assert "Pet" in result.output
