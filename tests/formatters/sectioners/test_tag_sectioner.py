import pytest

import npc
from npc.formatters.sectioners import TagSectioner

def test_uses_tag_data(prefs):
    sectioner = TagSectioner('type', 1, prefs)
    character = npc.Character(attributes={'type': ['changeling']})

    assert sectioner.text_for(character) == 'changeling'

def test_translates_tag(prefs):
    sectioner = TagSectioner('type-unit', 1, prefs)
    character = npc.Character(attributes={'type': ['changeling'], 'motley': ['fools']})

    assert sectioner.text_for(character) == 'fools'
