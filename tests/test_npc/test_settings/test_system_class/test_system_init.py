import pytest

from npc.settings import System, Settings

def test_sets_key():
    settings = Settings()

    system = System("generic", settings)

    assert system.key == "generic"

def test_sets_name():
    settings = Settings()

    system = System("generic", settings)

    assert system.name == settings.get("npc.systems.generic.name")

def test_sets_desc():
    settings = Settings()

    system = System("generic", settings)

    assert system.desc == settings.get("npc.systems.generic.desc")

def test_raises_on_bad_key():
    settings = Settings()

    with pytest.raises(KeyError):
        system = System("nope", settings)
