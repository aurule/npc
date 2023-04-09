import pytest
from tests.fixtures import fixture_file

from npc.settings import Settings

def test_loads_default_settings():
    settings = Settings()

    assert settings.get("npc.version") != ""

def test_loads_default_systems():
    settings = Settings()
    
    assert "nwod" in settings.get("npc.systems").keys()

@pytest.mark.xfail
def test_loads_default_types():
    settings = Settings()

    assert "changeling" in settings.get("npc.systems.nwod.types").keys()

def test_loads_personal_settings(tmp_path):
    settings = Settings(personal_dir = fixture_file("personal", "simple"))

    assert settings.get("npc.editor") == "custom"

def test_loads_personal_systems():
    settings = Settings(personal_dir = fixture_file("personal", "large"))

    assert "custom" in settings.get("npc.systems").keys()

@pytest.mark.xfail
def test_loads_personal_types():
    settings = Settings(personal_dir = fixture_file("personal", "chonk"))
    
    assert "pet" in settings.get("npc.systems.generic.types").keys()
