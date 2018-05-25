import npc
from npc.formatters.sectioners import BaseSectioner
import pytest
from unittest import mock

def fake_text_for(self, character):
    return 'asdf1234'

def test_text_for():
    sectioner = BaseSectioner(1, None)
    char = npc.Character()
    with pytest.raises(NotImplementedError):
        sectioner.text_for(char)

class TestWouldChange:
    def test_is_false_with_same_text(self):
        with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
            sectioner = npc.formatters.sectioners.BaseSectioner(1, None)
            sectioner.current_text = 'asdf1234'

            assert sectioner.would_change(None) is False

    def test_is_true_with_different_text(self):
        with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
            sectioner = npc.formatters.sectioners.BaseSectioner(1, None)
            sectioner.current_text = 'something else'

            assert sectioner.would_change(None) is True

def test_update_text_changes_text():
    with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
        sectioner = npc.formatters.sectioners.BaseSectioner(1, None)
        sectioner.current_text = 'something else'
        sectioner.update_text(None)

        assert sectioner.current_text == 'asdf1234'
