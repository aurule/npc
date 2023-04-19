from npc.settings import Settings, System

def test_loads_global_types():
    settings = Settings()
    system = settings.get_system("fate")

    system.load_types()

    assert "supporting" in settings.get("npc.types.fate")
