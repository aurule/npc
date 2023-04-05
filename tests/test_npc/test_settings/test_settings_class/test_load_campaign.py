import pytest
from tests.fixtures import fixture_file

from npc.settings import Settings

def test_loads_campaign_settings():
	settings = Settings()

	settings.load_campaign(fixture_file(["campaigns", "simple"]))

	assert "name" in settings.get("campaign")

def test_loads_campaign_systems():
	settings = Settings()

	settings.load_campaign(fixture_file(["campaigns", "large"]))

	assert "custom" in settings.get("npc.systems").keys()

@pytest.mark.xfail
def test_loads_campaign_types():
	settings = Settings()

	settings.load_campaign(fixture_file(["campaigns", "chonk"]))

	assert "pet" in settings.get("npc.systems.generic.types")
