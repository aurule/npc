import npc
import pytest
from tests.util import fixture_dir

# tests to do
# json loading ignores comments
# error prints arbitrary message to stderr
# flatten(['some text', 5, ['yet more']]) should yield ['some text', 5, 'yet more']
# find campaign root returns folder containing .npc or current directory if not found
# new class using Singleton yields the same object when created again:

def test_open_files(prefs):
    override_path = fixture_dir('util', 'open_files', 'settings-echo.json')
    prefs.load_more(override_path)
    result = npc.util.open_files('not a real path', 'seriously, no', prefs=prefs)
    assert 'not a real path' in result.args
    assert 'seriously, no' in result.args
