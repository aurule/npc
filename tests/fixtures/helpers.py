import os
import pytest
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from functools import wraps
from click.testing import CliRunner

from npc.campaign import init, Campaign

def fixture_file(*fixture_path: list[str]) -> Path:
    """Get the Path to a particular fixture

    This helper loads fixtures from the tests.fixtures module. It appends the given fixture_path items using
    importlib and returns the resulting pathlike object.

    Args:
        fixture_path (list[str]): One or more path components to append

    Returns:
        Path: Pathlike object referencing the named fixture
    """
    base: Path = resources.files("tests.fixtures")
    return base.joinpath(*fixture_path)

@pytest.fixture
def tmp_campaign(tmp_path: Path) -> Campaign:
    """Pytest fixture to supply a campaign object initialized to a temporary directory

    This initializes a blank campaign in a temporary path, suitable for keeping a test isolated. See
    campaign.init for what is created.

    Args:
        tmp_path (Path): Temporary path for the campaign, provided by the tmp_path pytest fixture

    Returns:
        Campaign: Campaign class rooted to tmp_path, with basic directories initialized
    """
    return init(tmp_path, name="Test Campaign", system="generic")

@contextmanager
def change_cwd(new_cwd: str):
    """Execute some code within the given directory

    Changes the working directory to new_cwd for a single with... block.

    Args:
        new_cwd (str): New CWD to use
    """
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

def isolated(func):
    """Decorator to isolate a test within its tmp_path or tmp_campaign's root

    Requires that the test args include either tmp_path or tmp_campaign.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        match kwargs:
            case {"tmp_campaign": campaign}:
                jail = campaign.root
            case {"tmp_path": tpath}:
                jail = tpath
        with change_cwd(jail):
            func(*args, **kwargs)
    return wrapper
