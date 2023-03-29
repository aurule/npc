"""Tests the changeling-specific validations"""

import npc
from npc.character import Werewolf
import pytest

only_one = [
    ('tribe', ['blood talons', 'hunters in darkness']),
    ('pack', ['townies', 'hillbillies']),
    ('lodge', ['some dudes', 'some other dudes']),
    ('auspice', ['rahu', 'cahalith'])
]
@pytest.mark.parametrize('key, values', only_one)
def test_single_tags(key, values):
    char = Werewolf(type=['werewolf'], **{key: values})
    char.validate(strict=True)
    assert "Too many values for tag '{}'. Limit of 1".format(key) in char.problems
