from npc.settings import Settings, System

def test_gets_global_types():
    settings = Settings()
    system = settings.get_system("fate")

    types = system.types

    assert "supporting" in types

def test_gets_inherited_types():
    settings = Settings()
    system = settings.get_system("fate-ep")

    types = system.types

    assert "supporting" in types
