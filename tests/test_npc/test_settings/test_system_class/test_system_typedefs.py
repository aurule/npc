from npc.settings import Settings, System

def test_gets_own_typedefs():
    settings = Settings()
    system = settings.get_system("fate")

    assert "supporting" in system.typedefs

def test_gets_parent_typedefs():
    settings = Settings()
    system = settings.get_system("fate-venture")

    assert "supporting" in system.typedefs
