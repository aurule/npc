import pytest
import npc
import os
from tests.util import fixture_dir

@pytest.fixture
def settings():
    return npc.main.Settings()

def test_creation(settings):
    assert settings is not None

def test_override(settings):
    override_path = fixture_dir(['settings/settings-vim.json'])
    old_editor = settings.get('editor')
    settings.load_more(override_path)
    assert settings.get('editor') != old_editor

def test_nested_get(settings):
    assert settings.get('paths.characters') == 'Characters'

def test_get_settings_path(settings):
    assert settings.get_settings_path('default') == os.path.join(settings.default_settings_path, 'settings-default.json')
    assert settings.get_settings_path('campaign') == os.path.join(settings.campaign_settings_path, 'settings.json')

def test_support_paths(settings):
    """Paths loaded from additional files should be expanded relative to that file"""
    override_path = fixture_dir(['settings/settings-paths.json'])
    settings.load_more(override_path)
    assert settings.get('support.testpath') == fixture_dir(['settings/nothing.json'])
