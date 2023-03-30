from pathlib import Path

def fixture_file(fixture_path: list[str]) -> Path:
    base: Path = Path(__file__).resolve().parent
    return base.joinpath(*fixture_path)
