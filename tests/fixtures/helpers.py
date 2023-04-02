from pathlib import Path
from importlib import resources

def fixture_file(fixture_path: list[str]) -> Path:
    base: Path = resources.files("tests.fixtures")
    return base.joinpath(*fixture_path)
