import npc
import pytest
import io
from collections import Counter
import re

from tests.util import fixture_dir

# sectioner
#   does nothing by default
#   when present, inserts sections appropriately
# progress
#   does nothing by default
#   called once per character when provided

class Listing:
    CHARACTER_NAMES = ['Tom', 'Matt', 'Paul', 'Vincent']
    CHARACTER_NAME_REGEX = r'^###\s(?P<name>.*)$'

    def __init__(self, **kwargs):
        self._output = io.StringIO()
        self.result = npc.formatters.markdown.listing(self.build_characters(), self._output, **kwargs)

    @property
    def output(self):
        return self._output.getvalue()

    def build_characters(self, names=None):
        if not names:
            names = self.CHARACTER_NAMES
        return [npc.Character({'name': [name]}) for name in names]

    def names_from_output(self):
        return set(re.findall(self.CHARACTER_NAME_REGEX, self.output, re.MULTILINE))

class TestBasicCorrectness:
    def test_includes_all_characters(self):
        listing = Listing()
        assert listing.result
        assert listing.names_from_output() - set(Listing.CHARACTER_NAMES) == set()

    def test_inserts_footer(self, prefs):
        prefs.load_more(fixture_dir('listing', 'markdown', 'footer', 'settings.json'))
        listing = Listing(prefs=prefs)
        assert listing.result
        assert "I'm footer content! Woohoo!" in listing.output

class TestIncludeMetadata:
    metadata = {'hello': 'friend'}

    @pytest.mark.parametrize('format_name', npc.formatters.markdown.SUPPORTED_METADATA_TYPES)
    def test_valid_formats(self, format_name):
        listing = Listing(include_metadata=format_name, metadata=self.metadata)
        assert listing.result
        with open(fixture_dir('listing', 'markdown', 'metadata', "metadata-{}.txt".format(format_name)), 'r') as f:
            assert f.read() in listing.output

    def test_invalid_format(self):
        listing = Listing(include_metadata='soap', metadata=self.metadata)
        assert listing.result.success == False

class TestPartialOption:
    metadata = {'hello': 'friend'}

    def test_hides_footer(self, prefs):
        prefs.load_more(fixture_dir('listing', 'markdown', 'footer', 'settings.json'))
        listing = Listing(partial=True, prefs=prefs)
        assert listing.result
        assert "I'm footer content! Woohoo!" not in listing.output

    def test_hides_metadata(self):
        listing = Listing(include_metadata='mmd', metadata=self.metadata, partial=True)
        assert listing.result
        assert "friend" not in listing.output

class TestSectioner:
    def test_no_default_sections(self):
        listing = Listing()
        assert listing.result
        assert re.search(r'^## .*$', listing.output, re.MULTILINE) is None

    def test_sectioner_is_inserted(self):
        listing = Listing(sectioner=lambda c: c.get_first('name', '').split(' ')[-1][0])
        assert listing.result
        sections = re.findall(r'^## .*$', listing.output, re.MULTILINE)
        assert sections is not None
        assert len(sections) == 4
