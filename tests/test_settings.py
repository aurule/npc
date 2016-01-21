import pytest
import npc
import os

@pytest.fixture
def settings():
    return npc.main.Settings()

@pytest.fixture
def override_path():
    base = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base, "fixtures/settings-vim.json")

def test_creation(settings):
    assert settings is not None

def test_override(settings, override_path):
    old_editor = settings.get('editor')
    settings.load_more(override_path)
    assert settings.get('editor') != old_editor

def test_nested_get(settings):
    assert settings.get('paths.characters') == 'Characters'

def test_get_settings_path(settings):
    assert settings.get_settings_path('default') == settings.path_default
