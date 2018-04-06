"""Tests the changeling-specific validations"""

import npc
import pytest

required_tags = ('auspice',)

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_present(tag):
    char = npc.Character(type=['werewolf'], **{tag: ['hi']})
    char.validate()
    assert 'Missing {}'.format(tag) not in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_not_present(tag):
    char = npc.Character(type=['werewolf'], **{tag: []})
    char.validate()
    assert 'Missing {}'.format(tag) in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_empty(tag):
    char = npc.Character(type=['werewolf'], **{tag: [' \t']})
    char.validate()
    assert 'Empty {}'.format(tag) in char.problems

only_one = [
    ('tribe', ['blood talons', 'hunters in darkness']),
    ('pack', ['townies', 'hillbillies']),
    ('lodge', ['some dudes', 'some other dudes'])
]
@pytest.mark.parametrize('key, values', only_one)
def test_single_tags(key, values):
    char = npc.Character(type=['werewolf'], **{key: values})
    char.validate()
    assert 'Multiple {key}s: {vals}'.format(key=key, vals=", ".join(values)) in char.problems
