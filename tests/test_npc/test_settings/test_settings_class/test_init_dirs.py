from tests.fixtures import fixture_file
from npc.settings import Settings

def test_has_required_dirs():
	settings = Settings()

	required_dirs = set(settings.required_dirs)
	init_dirs = set(settings.init_dirs)

	assert required_dirs.issubset(init_dirs)

def test_has_optional_dirs():
	settings = Settings()
	settings.load_settings_file(fixture_file("campaigns", "init_dirs", ".npc", "settings.yaml"))

	assert "hello" in settings.init_dirs
