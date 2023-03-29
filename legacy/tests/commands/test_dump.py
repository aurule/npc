import npc
import json
import pytest
from util import fixture_dir, load_json

@pytest.fixture
def list_json_output(tmp_path):
    def make_list(*search_parts, metadata=False, do_sort=False):
        outfile = tmp_path / 'output.json'
        search = fixture_dir('dump', *search_parts)

        npc.commands.dump(search, outfile=str(outfile), metadata=metadata, do_sort=do_sort)
        return load_json(outfile)
    return make_list

def test_valid_json(list_json_output):
    list_json_output()

def test_dump_matches_internal(list_json_output):
    dump_data = list_json_output()
    raw_data = npc.parser.get_characters(search_paths=[fixture_dir('dump')])
    tag_data = [c.dump() for c in raw_data]
    assert dump_data == list(tag_data)

def test_dump_stores_paths(list_json_output):
    dump_data = list_json_output()
    raw_data = npc.parser.get_characters(search_paths=[fixture_dir('dump')])
    assert dump_data[0]['path'] == list(raw_data)[0].path

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

def test_output_to_file(tmp_path):
    outfile = tmp_path / 'output.json'
    search = fixture_dir('dump')
    npc.commands.dump(search, outfile=str(outfile))
    assert outfile.read_text()

def test_directive(list_json_output):
    """Dump should contain literal value of directives"""

    data = list_json_output('Adrian Test.nwod')
    assert data[0]['faketype'][0] == 'Vampire'
