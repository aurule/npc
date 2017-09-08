import npc
import pytest
import sys
from tests.util import fixture_dir

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(capsys, outopt):
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing.make_list(search, outfile=outopt)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing.make_list(search, outfile=str(outfile))
    assert outfile.read()

def test_list_valid_json(list_json_output):
    """Ensure the 'json' output format yields valid JSON"""

     # no assert needed: the json module raises exceptions when parsing fails.
    list_json_output('valid-json')

def test_progress_callback(tmpdir, capsys):
    """The progress callback should be called for every character"""

    outfile = tmpdir.join("output.md")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing.make_list(search, fmt='markdown', outfile=str(outfile), progress=lambda i, t: print("{} of {}".format(i, t), file=sys.stderr))
    _, errtext = capsys.readouterr()
    assert "0 of 3\n1 of 3\n2 of 3\n3 of 3\n" == errtext
