from npc.settings import Settings, System

def test_with_parent_returns_system():
    settings = Settings()

    system = settings.get_system("fate-venture")
    parent_system = settings.get_system("fate")

    assert system.parent == parent_system

def test_without_parent_returns_none():
    settings = Settings()

    system = settings.get_system("nwod")

    assert system.parent is None
