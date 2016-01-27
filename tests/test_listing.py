import npc
import pytest
import json
from tests.util import fixture_dir

def test_list_valid_json(argparser, prefs, tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir(['listing'])
    args = argparser.parse_args(['list', '--search', search, '--format', 'json', '-o', str(outfile)])
    npc.commands.list(args, prefs)
    json.load(outfile) # no assert needed: the json module raises exceptions when parsing fails.

def test_skip():
    pass

def test_faketype():
    pass
