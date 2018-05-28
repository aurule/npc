import pytest

import npc
from npc.formatters.sectioners import LastInitialSectioner

def test_uses_tag_data(prefs):
    sectioner = LastInitialSectioner(1, prefs)
    character = npc.Character(attributes={'name': ['Bob Marley']})

    assert sectioner.text_for(character) == 'M'

def test_uses_first_name_with_no_last_name(prefs):
    sectioner = LastInitialSectioner(1, prefs)
    character = npc.Character(attributes={'name': ['Bob']})

    assert sectioner.text_for(character) == 'B'

def test_is_none_with_no_name(prefs):
    sectioner = LastInitialSectioner(1, prefs)
    character = npc.Character(attributes={'name': []})

    assert sectioner.text_for(character) is None

def test_is_none_with_empty_name(prefs):
    sectioner = LastInitialSectioner(1, prefs)
    character = npc.Character(attributes={'name': ['']})

    assert sectioner.text_for(character) is None
