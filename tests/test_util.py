import npc
from npc.util import Result
import pytest
from tests.util import fixture_dir

# tests to do
# json loading ignores comments
# error prints arbitrary message to stderr
# flatten(['some text', 5, ['yet more']]) should yield ['some text', 5, 'yet more']
# find campaign root returns folder containing .npc or current directory if not found

# json loading
#   ignores comments // and /*..*/
#   on bad syntax, reports a nice error string in err.nicemsg
#   if cannot load, includes nice error string in err.nicemsg
#
# error prints to stderr
#
# flatten handles mixed iterable types: flatten(['some text', 5, ['yet more']]) should yield ['some text', 5, 'yet more']
#
# find_campaign_root returns folder containing .npc or current directory if not found

def test_open_files(prefs):
    override_path = fixture_dir('util', 'open_files', 'settings-echo.json')
    prefs.load_more(override_path)
    result = npc.util.open_files('not a real path', 'seriously, no', prefs=prefs)
    assert 'not a real path' in result.args
    assert 'seriously, no' in result.args

class TestResult:
    def test_str_success(self):
        result = Result(True)
        assert str(Result) == "Success"

# Result
#   __str__ gives "Success" or self.errmsg
#   __bool__ gives self.success
