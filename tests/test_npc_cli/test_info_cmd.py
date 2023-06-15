from click.testing import CliRunner
from tests.fixtures import runner, tmp_campaign, isolated

from npc_cli import cli

@isolated
def test_aborts_on_missing_campaign(tmp_path, runner):
    result = runner.invoke(cli, 'info')

    assert "Not a campaign" in result.output

@isolated
def test_shows_campaign_name(tmp_campaign, runner):
    result = runner.invoke(cli, 'info')

    assert tmp_campaign.name in result.output
