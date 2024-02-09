from tests.fixtures import fixture_file

from npc.settings import Settings

def test_returns_systems_list():
	settings = Settings()

	systems = settings.systems

	system_keys = [s.key for s in systems]
	assert "nwod" in system_keys
