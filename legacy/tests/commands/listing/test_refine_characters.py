"""Tests the behavior of certain special tags and directives"""

import npc
import pytest
import json

from npc.commands.listing import _refine_characters
from npc.character import Character

def test_characters_with_skip_are_excluded():
    c1 = Character(type=['human'])
    c2 = Character(type=['human'], skip=True)

    charlist = list(_refine_characters([c1, c2]))

    assert c1 in charlist
    assert c2 not in charlist
