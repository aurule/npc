import pytest
import npc
from datetime import datetime
from tests.util import fixture_dir

def test_creation(prefs):
    assert prefs is not None

def test_override(prefs):
    override_path = fixture_dir('settings', 'settings-vim.json')
    old_editor = prefs.get('editor')
    prefs.load_more(override_path)
    assert prefs.get('editor') != old_editor

def test_nested_get(prefs):
    assert prefs.get('paths.required.characters') == 'Characters'

def test_nested_null_get(prefs):
    """A null key in the middle of a path should still just return None"""
    assert prefs.get('listing.templates.markdown.header.foobar') == None

def test_get_settings_path(prefs):
    assert prefs.get_settings_path('default') == prefs.default_settings_path.joinpath('settings-default.json')
    assert prefs.get_settings_path('campaign') == prefs.campaign_settings_path.joinpath('settings.json')

@pytest.mark.parametrize('settings_type', ['changeling', 'werewolf'])
def test_get_typed_settings_path(prefs, settings_type):
    fetched_path = prefs.get_settings_path('default', settings_type)
    assert fetched_path == prefs.default_settings_path.joinpath('settings-{}.json'.format(settings_type))

def test_expanded_paths(prefs):
    """Paths loaded from additional files should be expanded relative to that file"""
    override_path = fixture_dir('settings', 'settings-paths.json')
    prefs.load_more(override_path)
    assert prefs.get('types.changeling.sheet_template') == fixture_dir('settings', 'changeling.nwod')

def test_singleton_settings():
    prefs1 = npc.settings.InternalSettings()
    prefs2 = npc.settings.InternalSettings()
    assert prefs1 is prefs2

def test_available_types(prefs):
    names = prefs.get_available_types()
    assert set(names) == set(['human', 'fetch', 'changeling', 'goblin', 'werewolf', 'spirit', 'vampire'])

def test_update_key(prefs):
    prefs.update_key('paths.required.characters', 'nothing here')
    assert prefs.get('paths.required.characters') == 'nothing here'

class TestMetadata:
    """Tests the correctness of the metadata hash"""

    @pytest.fixture
    def get_metadata(self, prefs):
        def do_meta(meta_format=None):
            override_path = fixture_dir('settings', 'settings-metadata.json')
            prefs.load_more(override_path)
            if not meta_format:
                meta_format = prefs.get("listing.default_format")
            return prefs.get_metadata(meta_format)
        return do_meta

    def test_title(self, get_metadata):
        metadata = get_metadata()
        assert metadata["title"] == "List of Tests"

    def test_campaign(self, get_metadata):
        metadata = get_metadata()
        assert metadata["campaign"] == "Totally Recalled"

    def test_timestamp(self, get_metadata):
        reference_timestamp = datetime.now().strftime("%A %d %B")
        metadata = get_metadata()
        assert metadata["created"] == reference_timestamp

    def test_version(self, get_metadata):
        metadata = get_metadata()
        assert metadata["npc"] == npc.__version__.__version__

    @pytest.mark.parametrize('meta_format', ['markdown', 'json', 'html'])
    def test_additional_keys(self, get_metadata, meta_format):
        metadata = get_metadata(meta_format)
        assert metadata["test"] == "very yes"
        assert metadata["format"] == meta_format

class TestIgnoredPaths:
    def test_defaults_to_always_key(self, prefs):
        prefs.update_key('paths.ignore.always', ['abc123'])
        assert prefs.get_ignored_paths('dne') == ['abc123']

    def test_adds_by_command_name(self, prefs):
        prefs.update_key('paths.ignore.always', ['abc123'])
        prefs.update_key('paths.ignore.dne', ['something else'])
        assert set(prefs.get_ignored_paths('dne')) == set(['abc123', 'something else'])

@pytest.mark.parametrize('file_name', [
                                        'settings-default',
                                        'settings-changeling',
                                        'settings-werewolf',
                                        'settings-gui'])
def test_default_files_match(prefs, file_name):
    settings_file_base = prefs.default_settings_path.joinpath(file_name)
    loaded = [npc.util.load_settings(settings_file_base.with_suffix(s)) for s in prefs.settings_file_suffixes]
    assert loaded[1:] == loaded[:-1]
