import npc
import pytest
import io
from collections import Counter

from tests.util import fixture_dir

def test_default_table_format():
    data_out = io.StringIO()
    tables = {
        'type': Counter(['human', 'human', 'elf'])
    }
    assert npc.formatters.markdown.report(tables, data_out)

    with open(fixture_dir('formatters', 'markdown', 'report.txt')) as table_fixture:
        assert data_out.getvalue() == table_fixture.read()
