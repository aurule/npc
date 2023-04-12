from tests.fixtures import fixture_file

from npc.settings import Settings

def test_returns_keys_list():
	settings = Settings()

	assert "nwod" in settings.get_system_keys()
