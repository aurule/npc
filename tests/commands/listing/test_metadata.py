"""Tests the handling of metadata and related settings"""

import npc
import pytest
from tests.util import fixture_dir
import re

@pytest.mark.parametrize('metaformat', ['json', 'asdf'])
def test_json_metadata(list_json_output, metaformat):
    """The json output should include an object with metadata keys when the
    metadata arg is supplied, regardless of its value."""

    listing = list_json_output('valid-json', metadata=metaformat)
    for c in listing:
        if 'meta' in c:
            assert c['meta'] == True
            assert c['title'] == 'NPC Listing'
            assert 'created' in c

def test_md_mmd_metadata(tmpdir):
    """The 'mmd' metadata arg should prepend multi-markdown metadata tags to
    the markdown output."""

    outfile = tmpdir.join("output.md")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing.make_list(search, fmt='markdown', metadata='mmd', outfile=str(outfile))
    assert 'Title: NPC Listing' in outfile.read()

@pytest.mark.parametrize('metaformat', ['yfm', 'yaml'])
def test_md_yfm_metadata(metaformat, tmpdir):
    """The 'yfm' and 'yaml' metadata args should both result in YAML front
    matter being prepended to markdown output."""

    outfile = tmpdir.join("output.md")
    search = fixture_dir('listing', 'valid-json')
    npc.commands.listing.make_list(search, fmt='markdown', metadata=metaformat, outfile=str(outfile))
    match = re.match(r'(?sm)\s*---(.*)---\s*', outfile.read())
    assert match is not None
    assert 'title: NPC Listing' in match.group(1)

def test_extra_json_metadata(list_json_output, prefs):
    """The extra json metdata should be included for the json output type."""
    prefs.load_more(fixture_dir('listing', 'settings-metadata.json'))
    listing = list_json_output('valid-json', metadata='json', prefs=prefs)
    for c in listing:
        if 'meta' in c:
            assert c['test'] == 'yes'
            assert c['test-type'] == 'json'

@pytest.mark.parametrize('metaformat', ['mmd', 'yfm', 'yaml'])
def test_extra_md_metadata(prefs, metaformat, tmpdir):
    """All metadata formats for the markdown type should show the extra
    metadata for the markdown type from the imported settings."""

    outfile = tmpdir.join("output.md")
    prefs.load_more(fixture_dir('listing', 'settings-metadata.json'))
    search = fixture_dir('listing', 'valid-json')
    result = npc.commands.listing.make_list(search, fmt='markdown', metadata=metaformat, outfile=str(outfile), prefs=prefs)
    assert result.errmsg == ''
    assert result.success == True
    assert 'test-type: markdown' in outfile.read().lower()

def test_invalid_metadata_arg():
    """Using metadata formats other than yfm and mmd is not supported for
    the markdown output type.

    The json output type ignores the format argument entirely, which is not
    tested.
    """
    search = fixture_dir('listing', 'valid-json')
    result = npc.commands.listing.make_list(search, fmt='md', metadata='json')
    assert not result.success

def test_unknown_metadata_arg():
    """Unrecognized metadata options should result in an error"""
    search = fixture_dir('listing', 'valid-json')
    result = npc.commands.listing.make_list(search, fmt='md', metadata='asdf')
    assert not result.success

def test_custom_title(list_json_output):
    listing = list_json_output('valid-json', metadata=True, title="I'm a test list")
    for part in listing:
        if 'meta' in part:
            assert part['title'] == "I'm a test list"
