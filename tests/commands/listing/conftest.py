import npc
import pytest
from tests.util import fixture_dir, load_json
import json

@pytest.fixture
def list_json_output(tmp_path, prefs):
    def make_list(*search_parts, outformat='json', metadata=None, prefs=prefs, title=None):
        tmpdir = tmp_path / 'list'
        tmpdir.mkdir()
        outfile = tmpdir / 'output.json'
        outfile.touch()
        search = fixture_dir('listing', *search_parts)
        npc.commands.listing.make_list(search, fmt=outformat, metadata=metadata, outfile=str(outfile), prefs=prefs, title=title)
        return load_json(outfile)
    return make_list
