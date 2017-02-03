import npc
import pytest
from tests.util import fixture_dir
import json

@pytest.fixture(scope="module")
def list_json_output(tmpdir_factory, prefs):
    def make_list(*search_parts, outformat='json', metadata=None, prefs=prefs, title=None):
        tmpdir = tmpdir_factory.mktemp('list')
        outfile = tmpdir.join("output.json")
        search = fixture_dir('listing', *search_parts)
        npc.commands.listing.make_list(search, fmt=outformat, metadata=metadata, outfile=str(outfile), prefs=prefs, title=title)
        return json.load(outfile)
    return make_list
