from pathlib import Path
import json

def fixture_dir(*dirnames):
    """
    Get the path to some fixtures.

    Args:
        *dirnames (str): Any number of path elements within /fixtures/

    Returns:
        Path object
    """

    base = Path(__file__).resolve().parent
    return base.joinpath('fixtures', *dirnames)

def load_json(pathlib_path):
    with open(pathlib_path, 'r') as f:
        return json.load(f)
