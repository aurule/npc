import pytest
from pathlib import Path
from importlib import resources

from npc.campaign import init, Campaign

def fixture_file(fixture_path: list[str]) -> Path:
    base: Path = resources.files("tests.fixtures")
    return base.joinpath(*fixture_path)

@pytest.fixture
def tmp_campaign(tmp_path):
    return init(tmp_path, name="Test Campaign", system="generic")
