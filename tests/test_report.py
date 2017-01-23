import npc
import pytest
import json
from tests.util import fixture_dir

@pytest.fixture
def report_json_output(tmpdir, prefs):
    def make_report(tags, *search_parts, outformat='json', prefs=prefs):
        outfile = tmpdir.join("output.json")
        search = fixture_dir('report', *search_parts)
        npc.commands.report(tags, search=[search], fmt=outformat, outfile=str(outfile), prefs=prefs)
        return json.load(outfile)
    return make_report

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(capsys, outopt):
    search = fixture_dir('report', 'valid-json')
    npc.commands.report('type', search=[search], outfile=outopt)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.report('type', search=[search], outfile=str(outfile))
    assert outfile.read()

def test_list_valid_json(report_json_output):
    """Ensure the 'json' output format yields valid JSON"""

     # no assert needed: the json module raises exceptions when parsing fails.
    report_json_output('type', 'valid-json')

def test_basic_count(report_json_output):
    report = report_json_output('type', 'count-types')
    assert report['type']['Human'] == 3
    assert report['type']['Changeling'] == 2
