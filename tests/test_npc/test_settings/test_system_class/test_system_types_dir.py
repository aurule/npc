from npc.settings import Settings, System

def test_returns_proper_dir():
    settings = Settings()
    system = settings.get_system("fate")

    assert system.types_dir == settings.default_settings_path / "types" / "fate"
