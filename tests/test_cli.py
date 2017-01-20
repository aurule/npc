import npc
import pytest
import subprocess

@pytest.fixture
def run():
    def do_run(*args):
        args = ["python", "npc.py"] + list(args)
        return subprocess.run(args, stdout=subprocess.PIPE)
    return do_run

# tests to do:
# finds the correct campaign root if not given
# fails gracefully when given an invalid campaign path
# shows problems from settings lint
# shows help when no command given
# shows error message when command fails
# batch option suppresses printed output
# batch option suppresses file opening
