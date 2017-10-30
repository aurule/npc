import npc
import pytest
import io
from collections import Counter

from tests.util import fixture_dir

def test_default_table_format():
    data_out = io.BytesIO()
    tables = {
        'type': Counter(['human', 'human', 'elf'])
    }
    assert npc.formatters.html.report(tables, data_out)

    with open(fixture_dir('formatters', 'html', 'report.txt')) as table_fixture:
        assert data_out.getvalue().decode() == table_fixture.read()
