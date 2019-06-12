"""Tests the spirit-specific validations"""

import npc
from npc.character import Spirit
import pytest

required_tags = ('ban',)

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_present(tag):
    char = Spirit(type=['spirit'], **{tag: ['hi']})
    char.validate()
    assert "No values for tag '{}'".format(tag) not in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_not_present(tag):
    char = Spirit(type=['spirit'], **{tag: []})
    char.validate()
    assert "No values for tag '{}'".format(tag) in char.problems

@pytest.mark.parametrize('tag', required_tags)
def test_required_tag_empty(tag):
    char = Spirit(type=['spirit'], **{tag: [' \t']})
    char.validate()
    assert "No values for tag '{}'".format(tag) in char.problems
