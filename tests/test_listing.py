import npc
import pytest
import json
from tests.util import fixture_dir
import re

@pytest.fixture
def list_json_output(tmpdir, prefs):
    def make_list(search_parts, outformat='json', metadata=None, prefs=prefs):
        outfile = tmpdir.join("output.json")
        search = fixture_dir(['listing'] + search_parts)
        npc.commands.list([search], format=outformat, metadata=metadata, outfile=str(outfile), prefs=prefs)
        return json.load(outfile)
    return make_list

@pytest.mark.parametrize('outopt', [None, '-'])
def test_output_no_file(capsys, outopt):
    search = fixture_dir(['listing', 'valid-json'])
    npc.commands.list([search], outfile=outopt)
    output, _ = capsys.readouterr()
    assert output

def test_output_to_file(tmpdir):
    outfile = tmpdir.join("output.json")
    search = fixture_dir(['listing', 'valid-json'])
    npc.commands.list([search], outfile=str(outfile))
    assert outfile.read()

def test_list_valid_json(list_json_output):
    """Ensure the 'json' output format yields valid JSON"""

     # no assert needed: the json module raises exceptions when parsing fails.
    list_json_output(['valid-json'])

class TestBehavior:
    """Tests the behavior of certain special tags and directives"""

    def test_skip(self, list_json_output):
        """Characters with the @skip tag should be omitted from the output"""

        listing = list_json_output(['skip'])
        assert len(listing) == 1

    def test_faketype(self, list_json_output):
        """The value of @faketype should replace the value of @type"""

        listing = list_json_output(['faketype'])
        for c in listing:
            assert len(c['type']) == 1
            assert c['type'][0] == 'Human'

class TestMetadata:
    """Tests the handling of metadata and related settings"""

    @pytest.mark.parametrize('metaformat', ['json', 'asdf'])
    def test_json_metadata(self, list_json_output, metaformat):
        """The json output should include an object with metadata keys when the
        metadata arg is supplied, regardless of its value."""

        listing = list_json_output(['valid-json'], metadata=metaformat)
        for c in listing:
            if 'meta' in c:
                assert c['meta'] == True
                assert c['title'] == 'NPC Listing'
                assert 'created' in c

    def test_md_mmd_metadata(self, tmpdir):
        """The 'mmd' metadata arg should prepend multi-markdown metadata tags to
        the markdown output."""

        outfile = tmpdir.join("output.md")
        search = fixture_dir(['listing', 'valid-json'])
        npc.commands.list([search], format='markdown', metadata='mmd', outfile=str(outfile))
        assert 'Title: NPC Listing' in outfile.read()

    @pytest.mark.parametrize('metaformat', ['yfm', 'yaml'])
    def test_md_yfm_metadata(self, metaformat, tmpdir):
        """The 'yfm' and 'yaml' metadata args should both result in YAML front
        matter being prepended to markdown output."""

        outfile = tmpdir.join("output.md")
        search = fixture_dir(['listing', 'valid-json'])
        npc.commands.list([search], format='markdown', metadata=metaformat, outfile=str(outfile))
        match = re.match('(?sm)\s*---(.*)---\s*', outfile.read())
        assert match is not None
        assert 'title: NPC Listing' in match.group(1)

    def test_extra_json_metadata(self, list_json_output, prefs):
        """The extra json metdata should be included for the json output type."""
        prefs.load_more(fixture_dir(['listing', 'settings-metadata.json']))
        listing = list_json_output(['valid-json'], metadata='json', prefs=prefs)
        for c in listing:
            if 'meta' in c:
                assert c['test'] == 'yes'
                assert c['test-type'] == 'json'

    @pytest.mark.parametrize('metaformat', ['mmd', 'yfm', 'yaml'])
    def test_extra_md_metadata(self, prefs, metaformat, tmpdir):
        """All metadata formats for the markdown type should show the extra
        metadata for the markdown type from the imported settings."""

        outfile = tmpdir.join("output.md")
        prefs.load_more(fixture_dir(['listing', 'settings-metadata.json']))
        search = fixture_dir(['listing', 'valid-json'])
        npc.commands.list([search], format='markdown', metadata=metaformat, outfile=str(outfile), prefs=prefs)
        assert 'test-type: markdown' in outfile.read().lower()

    def test_invalid_metadata_arg(self, argparser):
        """Using metadata formats other than yfm and mmd is not supported for
        the markdown output type.

        The json output type ignores the format argument entirely, which is not
        tested.
        """
        search = fixture_dir(['listing', 'valid-json'])
        result = npc.commands.list([search], format='md', metadata='json')
        assert not result.success

    def test_unknown_metadata_arg(self, argparser):
        """Unrecognized metadata options should result in an error"""
        search = fixture_dir(['listing', 'valid-json'])
        result = npc.commands.list([search], format='md', metadata='asdf')
        assert not result.success
