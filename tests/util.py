import os

def fixture_dir(dirnames):
    """Get the path to some fixtures. Expects an array of path components."""

    base = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base, 'fixtures', *dirnames)
