from npc.settings import Settings

def test_returns_none_on_bad_key():
    settings = Settings()

    system = settings.get_system("nope")

    assert system is None

def test_returns_system_for_key():
    settings = Settings()

    system = settings.get_system("generic")

    assert system.name == settings.get("npc.systems.generic.name")
