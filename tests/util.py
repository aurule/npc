import os
import json

def fixture_dir(*dirnames):
    """
    Get the path to some fixtures.

    Args:
        *dirnames (str): Any number of path elements within /fixtures/

    Returns:
        Path object
    """

    base = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base, 'fixtures', *dirnames)

def load_json(pathlib_path):
    with open(pathlib_path) as f:
        return json.load(f)
