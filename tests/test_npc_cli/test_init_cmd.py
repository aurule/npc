from pathlib import Path
from click.testing import CliRunner
from tests.fixtures import runner, isolated

from npc_cli import cli

@isolated
def test_defaults_to_current_dir(tmp_path, runner):
    result = runner.invoke(cli, "init --system fate")

    assert result.exit_code == 0
    assert tmp_path.joinpath(".npc").exists()

@isolated
def test_accepts_target_dir(tmp_path, runner):
    result = runner.invoke(cli, "init campaign --system fate")

    assert result.exit_code == 0
    assert tmp_path.joinpath("campaign", ".npc").exists()

@isolated
def test_lists_dirs_to_create(tmp_path, runner):
    result = runner.invoke(cli, "init campaign --system fate")

    assert result.exit_code == 0
    assert "Session History" in result.output
