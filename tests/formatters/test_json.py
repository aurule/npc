import npc
import pytest
import io
import json

class TestListing:
    def test_listing_is_correct(self, character):
        characters = [character]
        data_out = io.StringIO()
        assert npc.formatters.json.listing(characters, data_out)

        parsed_data = json.loads(data_out.getvalue())
        assert parsed_data == characters

    def test_metadata_included(self, character):
        metadata = {'hello': 'friend'}
        data_out = io.StringIO()
        assert npc.formatters.json.listing([character], data_out, include_metadata=True, metadata=metadata)

        metadata['meta'] = True
        parsed_data = json.loads(data_out.getvalue())
        assert parsed_data == [metadata, character]

class TestReport:
    def test_report_is_correct(self):
        table = {
            "hero": "1",
            "mook": "300",
            "bystander": "500"
        }
        data_out = io.StringIO()
        assert npc.formatters.json.report(table, data_out)

        parsed_data = json.loads(data_out.getvalue())
        assert parsed_data == table
