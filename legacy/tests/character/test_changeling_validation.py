"""Tests the changeling-specific validations"""

import npc
from npc.character import Changeling
import pytest

required_tags = ('seeming', 'kith')

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_present(tag):
    char = Changeling(type=['changeling'], **{tag: ['hi']})
    char.validate()
    assert "No values for tag '{}'".format(tag) not in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_not_present(tag):
    char = Changeling(type=['changeling'], **{tag: []})
    char.validate()
    assert "No values for tag '{}'".format(tag) in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_empty(tag):
    char = Changeling(type=['changeling'], **{tag: [' \t']})
    char.validate()
    assert "No values for tag '{}'".format(tag) in char.problems

only_one = [
    ('court', ['summer', 'winter']),
    ('motley', ['townies', 'hillbillies']),
    ('entitlement', ['honorable knights', 'dishonorable knights'])
]
@pytest.mark.parametrize('key, values', only_one)
def test_single_tags(key, values):
    char = Changeling(type=['changeling'], **{key: values})
    char.validate(strict=True)
    assert "Too many values for tag '{}'. Limit of 1".format(key) in char.problems
