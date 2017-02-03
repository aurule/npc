"""Tests the behavior of certain special tags and directives"""

import npc
import pytest
import json
from tests.util import fixture_dir

def test_skip(list_json_output):
    """Characters with the @skip tag should be omitted from the output"""

    listing = list_json_output('skip')
    assert len(listing) == 1

def test_faketype(list_json_output):
    """The value of @faketype should replace the value of @type"""

    listing = list_json_output('faketype')
    for c in listing:
        assert len(c['type']) == 1
        assert c['type'][0] == 'Human'

def test_hide(list_json_output):
    """The fields named in @hide should not appear"""

    listing = list_json_output('hide')
    assert 'foreign' not in listing[0]

def test_hide_group(list_json_output):
    """The groups named in @hidegroup should not appear"""

    listing = list_json_output('hidegroup')
    assert 'Lawbros' not in listing[0]['group']

def test_hide_ranks(list_json_output):
    """The ranks for the groups named in @hiderank should not appear"""

    listing = list_json_output('hideranks')
    assert 'Big Corporation Place Thing' not in listing[0]['rank']
