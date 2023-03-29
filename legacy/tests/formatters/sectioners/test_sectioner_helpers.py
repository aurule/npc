import npc
import pytest

class TestGetSectioner:
    def test_get_last_initial_sectioner(self):
        sectioner = npc.formatters.sectioners.get_sectioner('last', 1, None)
        assert isinstance(sectioner, npc.formatters.sectioners.LastInitialSectioner)

    def test_get_tag_sectioner(self):
        sectioner = npc.formatters.sectioners.get_sectioner('type', 1, None)
        assert isinstance(sectioner, npc.formatters.sectioners.TagSectioner)
