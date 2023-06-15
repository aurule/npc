import os
import pytest
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from functools import wraps
from click.testing import CliRunner

from npc.campaign import init, Campaign

def fixture_file(*fixture_path) -> Path:
    base: Path = resources.files("tests.fixtures")
    return base.joinpath(*fixture_path)

@pytest.fixture
def tmp_campaign(tmp_path: Path) -> Campaign:
    return init(tmp_path, name="Test Campaign", system="generic")

@contextmanager
def change_cwd(new_cwd):
    old_cwd = os.getcwd()
    os.chdir(new_cwd)
    try:
        yield
    finally:
        os.chdir(old_cwd)

@pytest.fixture
def runner() -> CliRunner:
    """Fixture that provides a CliRunner object"""
    return CliRunner()
