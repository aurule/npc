from click.testing import CliRunner
from tests.fixtures import tmp_campaign

from npc_cli import cli

def test_shows_system_name(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ['describe', 'system', '-s', 'fate'])

    assert "Fate Core" in result.output

def test_shows_current_campaign_system(tmp_campaign):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_campaign.root):
        result = runner.invoke(cli, ['describe', 'system'])

    assert "Generic" in result.output

def test_includes_links(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ['describe', 'system', '-s', 'fate'])

    assert "http" in result.output
