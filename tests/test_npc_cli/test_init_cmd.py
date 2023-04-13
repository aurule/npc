from pathlib import Path
from click.testing import CliRunner

from npc_cli import cli

def test_defaults_to_current_dir(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(cli, ["init", "--system", "fate"])

        assert result.exit_code == 0
        assert Path(td).joinpath(".npc").exists()

def test_accepts_target_dir(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(cli, ["init", "campaign", "--system", "fate"])

        assert result.exit_code == 0
        assert Path(td).joinpath("campaign", ".npc").exists()

def test_lists_dirs_to_create(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["init", "campaign", "--system", "fate"])

        assert result.exit_code == 0
        assert "Session History" in result.output
