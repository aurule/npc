import npc
import json
import pytest
from tests.util import fixture_dir

@pytest.fixture
def list_json_output(tmpdir, argparser, prefs):
    def make_list(search_parts=[], metadata=False, sorted=False, prefs=prefs):
        outfile = tmpdir.join("output.json")
        search = fixture_dir(['dump'] + search_parts)
        arglist = [
            'dump',
            '--search', search,
            '-o', str(outfile)
        ]
        if metadata:
            arglist.append('--metadata')
        if sorted:
            arglist.append('--sort')

        args = argparser.parse_args(arglist)
        npc.commands.dump(args, prefs)
        return json.load(outfile)
    return make_list

def test_valid_json(list_json_output):
    list_json_output()

def test_dump_matches_internal(list_json_output):
    dump_data = list_json_output()
    raw_data = npc.parser.get_characters(search_paths=[fixture_dir(['dump'])])
    assert dump_data == list(raw_data)

def test_sort(list_json_output):
    """Tests that the dumped, sorted output identical to the internal sorted data"""
    raw_data = npc.parser.get_characters(search_paths=[fixture_dir(['dump'])])
    sorted_data = npc.commands._sort_chars(raw_data)
    dump_data = list_json_output(sorted=True)
    it = iter(sorted_data)
    with pytest.raises(StopIteration) as e:
        i = next(it)
        for x in dump_data:
            if x == i:
                i = next(it)

def test_metadata(list_json_output):
    """The json output should include an object with metadata keys when the
    metadata arg is supplied, regardless of its value."""

    listing = list_json_output(['valid-json'], metadata=True)
    for c in listing:
        if 'meta' in c:
            assert c['meta'] == True
            assert c['title'] == 'NPC Listing'
            assert 'created' in c

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(argparser, prefs, capsys, outopt):
    search = fixture_dir(['dump'])
    args = argparser.parse_args([
        'dump',
        '--search', search,
        '-o', outopt
    ])
    npc.commands.dump(args, prefs)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(argparser, prefs, tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir(['dump'])
    args = argparser.parse_args([
        'dump',
        '--search', search,
        '-o', str(outfile)
    ])
    npc.commands.dump(args, prefs)
    assert outfile.read()

def test_directive(list_json_output):
    """Dump should contain literal value of directives"""

    data = list_json_output(['Adrian Test.nwod'])
    assert data[0]['faketype'][0] == 'Vampire'
