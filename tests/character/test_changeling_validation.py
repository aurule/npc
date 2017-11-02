"""Tests the changeling-specific validations"""

import npc
import pytest

required_tags = ('seeming', 'kith')

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_present(tag):
    char = npc.Character(type=['changeling'], **{tag: ['hi']})
    char.validate()
    assert 'Missing {}'.format(tag) not in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_not_present(tag):
    char = npc.Character(type=['changeling'], **{tag: []})
    char.validate()
    assert 'Missing {}'.format(tag) in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_empty(tag):
    char = npc.Character(type=['changeling'], **{tag: [' \t']})
    char.validate()
    assert 'Empty {}'.format(tag) in char.problems

only_one = [
    ('court', ['summer', 'winter']),
    ('motley', ['townies', 'hillbillies']),
    ('entitlement', ['honorable knights', 'dishonorable knights'])
]
@pytest.mark.parametrize('key, values', only_one)
def test_many_courts(key, values):
    char = npc.Character(type=['changeling'], **{key: values})
    char.validate()
    assert 'Multiple {key}s: {vals}'.format(key=key, vals=", ".join(values)) in char.problems
