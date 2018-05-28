import npc
import json
import pytest
from tests.util import fixture_dir

@pytest.fixture
def list_json_output(tmpdir):
    def make_list(*search_parts, metadata=False, do_sort=False):
        outfile = tmpdir.join("output.json")
        search = fixture_dir('dump', *search_parts)

        npc.commands.dump(search, outfile=str(outfile), metadata=metadata, do_sort=do_sort)
        return json.load(outfile)
    return make_list

def test_valid_json(list_json_output):
    list_json_output()

def test_dump_matches_internal(list_json_output):
    dump_data = list_json_output()
    raw_data = npc.parser.get_characters(search_paths=[fixture_dir('dump')])
    assert dump_data == list(raw_data)

def test_metadata(list_json_output):
    """The json output should include an object with metadata keys when the
    metadata arg is supplied, regardless of its value."""

    listing = list_json_output('valid-json', metadata=True)
    for c in listing:
        if 'meta' in c:
            assert c['meta'] == True
            assert c['title'] == 'NPC Listing'
            assert 'created' in c

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(capsys, outopt):
    search = fixture_dir('dump')
    npc.commands.dump(search, outfile=outopt)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir('dump')
    npc.commands.dump(search, outfile=str(outfile))
    assert outfile.read()

def test_directive(list_json_output):
    """Dump should contain literal value of directives"""

    data = list_json_output('Adrian Test.nwod')
    assert data[0]['faketype'][0] == 'Vampire'
