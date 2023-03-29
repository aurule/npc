import npc
import pytest
import io
from collections import Counter
import re

from util import fixture_dir

class Listing:
    CHARACTER_NAMES = ['Tom', 'Matt', 'Paul', 'Vincent']
    CHARACTER_NAME_REGEX = r'^<h3>(?P<name>.*)</h3>$'
    SECTION_REGEX = r'^<h2>.</h2>$'

    def __init__(self, **kwargs):
        self._output = io.BytesIO()
        self.result = npc.formatters.html.listing(self.build_characters(), self._output, **kwargs)

    @property
    def output(self):
        return self._output.getvalue().decode()

    @property
    def sections(self):
        return re.findall(self.SECTION_REGEX, self.output, re.MULTILINE)

    def build_characters(self, names=None):
        if not names:
            names = self.CHARACTER_NAMES
        return [npc.character.Character({'name': [name]}) for name in names]

    def names_from_output(self):
        return set(re.findall(self.CHARACTER_NAME_REGEX, self.output, re.MULTILINE))

class TestBasicCorrectness:
    def test_includes_all_characters(self):
        listing = Listing()
        assert listing.result
        assert listing.names_from_output() - set(Listing.CHARACTER_NAMES) == set()

    def test_inserts_footer(self, prefs):
        prefs.load_more(fixture_dir('listing', 'html', 'footer', 'settings.json'))
        listing = Listing(prefs=prefs)
        assert listing.result
        assert "I'm footer content! Woohoo!" in listing.output

class TestIncludeMetadata:
    metadata = {'hello': 'friend'}

    @pytest.mark.parametrize('format_name', npc.formatters.html.SUPPORTED_METADATA_TYPES)
    def test_valid_formats(self, format_name):
        listing = Listing(metadata_format=format_name, metadata=self.metadata)
        assert listing.result
        with open(fixture_dir('listing', 'html', 'metadata', "metadata-{}.txt".format(format_name)), 'r') as f:
            assert f.read() in listing.output

    def test_invalid_format(self):
        listing = Listing(metadata_format='soap', metadata=self.metadata)
        assert listing.result.success == False

class TestPartialOption:
    metadata = {'hello': 'friend'}

    def test_hides_footer(self, prefs):
        prefs.load_more(fixture_dir('listing', 'html', 'footer', 'settings.json'))
        listing = Listing(partial=True, prefs=prefs)
        assert listing.result
        assert "I'm footer content! Woohoo!" not in listing.output

    def test_hides_metadata(self):
        listing = Listing(metadata_format='meta', metadata=self.metadata, partial=True)
        assert listing.result
        assert "friend" not in listing.output
