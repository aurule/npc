from npc.settings import Settings, System

def test_returns_proper_dir():
    settings = Settings()
    system = settings.get_system("fate")

    assert system.personal_types_dir == settings.personal_dir / "types" / "fate"
