from npc.settings import Settings, System

def test_gets_global_types():
    settings = Settings()
    system = settings.get_system("fate")

    chartype = system.get_type("supporting")

    assert chartype.name == "Supporting"

def test_gets_inherited_types():
    settings = Settings()
    system = settings.get_system("fate-ep")

    chartype = system.get_type("supporting")

    assert chartype.name == "Supporting"
