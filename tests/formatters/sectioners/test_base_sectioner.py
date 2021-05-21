import pytest
from unittest import mock

import mako
import npc
from npc.formatters.sectioners import BaseSectioner

def fake_text_for(self, character):
    return 'asdf1234'

def test_text_for():
    sectioner = BaseSectioner(1, None)
    char = npc.character.Character()
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

class TestTemplate:
    def test_retrieves_from_cache(self, prefs):
        with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
            sectioner = npc.formatters.sectioners.BaseSectioner(1, prefs)
            sectioner.templates_cache['html'] = 'placeholder text'

            assert sectioner.template('html') == 'placeholder text'

    def test_stores_template_to_cache(self, prefs):
        with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
            sectioner = npc.formatters.sectioners.BaseSectioner(1, prefs)

            template = sectioner.template('html')

            assert sectioner.templates_cache['html'] == template

    def test_gets_correct_template(self, prefs):
        with mock.patch.object(BaseSectioner, 'text_for', fake_text_for):
            sectioner = npc.formatters.sectioners.BaseSectioner(1, prefs)

            template = sectioner.template('html')

            assert isinstance(template, mako.template.Template)
            assert template.filename == str(prefs.get('listing.templates.html.sections.simple'))
