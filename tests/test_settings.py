import pytest
import npc
import os
from tests.util import fixture_dir

def test_creation(prefs):
    assert prefs is not None

def test_override(prefs):
    override_path = fixture_dir('settings', 'settings-vim.json')
    old_editor = prefs.get('editor')
    prefs.load_more(override_path)
    assert prefs.get('editor') != old_editor

def test_nested_get(prefs):
    assert prefs.get('paths.characters') == 'Characters'

def test_get_settings_path(prefs):
    assert prefs.get_settings_path('default') == os.path.join(prefs.default_settings_path, 'settings-default.json')
    assert prefs.get_settings_path('campaign') == os.path.join(prefs.campaign_settings_path, 'settings.json')

@pytest.mark.parametrize('settings_type', ['changeling', 'werewolf'])
def test_get_typed_settings_path(prefs, settings_type):
    fetched_path = prefs.get_settings_path('default', settings_type)
    assert fetched_path == os.path.join(prefs.default_settings_path, 'settings-{}.json'.format(settings_type))

def test_support_paths(prefs):
    """Paths loaded from additional files should be expanded relative to that file"""
    override_path = fixture_dir('settings', 'settings-paths.json')
    prefs.load_more(override_path)
    assert prefs.get('support.testpath') == fixture_dir('settings', 'nothing.json')
