from tests.fixtures import fixture_file

from npc.settings import Settings

def test_loads_regular_system():
	settings = Settings()

	assert "name" in settings.get("npc.systems.nwod").keys()

def test_allows_inherited_attributes():
	settings = Settings()

	assert "concept" in settings.get("npc.systems.fate-venture.tags").keys()

def test_skips_on_unknown_parent():
	settings = Settings()

	settings.load_systems(fixture_file("systems", "missing"))

	assert "missing_parent" not in settings.get("npc.systems").keys()

def test_allows_deep_inheritance():
	settings = Settings()
	
	settings.load_systems(fixture_file("systems", "multi"))

	assert "first" in settings.get("npc.systems").keys()

def test_does_not_choke_on_circular_extends():
	settings = Settings()

	settings.load_systems(fixture_file("systems", "circular"))
	
	assert "name" in settings.get("npc.systems.nwod").keys()

def test_skips_invalid_files():
	settings = Settings()

	settings.load_systems(fixture_file("systems", "invalid"))

	assert "invalid" not in settings.get("npc.systems").keys()
