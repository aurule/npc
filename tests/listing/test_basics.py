import npc
import pytest
from tests.util import fixture_dir

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(capsys, outopt):
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing(search, outfile=outopt)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing(search, outfile=str(outfile))
    assert outfile.read()

def test_list_valid_json(list_json_output):
    """Ensure the 'json' output format yields valid JSON"""

     # no assert needed: the json module raises exceptions when parsing fails.
    list_json_output('valid-json')
