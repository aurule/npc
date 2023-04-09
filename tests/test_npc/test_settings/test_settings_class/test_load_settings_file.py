from tests.fixtures import fixture_file

from npc.settings import Settings

def test_loads_valid_settings():
    settings = Settings()

    settings.load_settings_file(fixture_file("valid.yaml"))

    assert settings.get("valid") == True

def test_ignores_missing_files(tmp_path):
    settings = Settings()

    settings.load_settings_file(tmp_path / "missing.yaml")

    assert settings.get("npc.version")

def test_ignores_parse_errors():
    settings = Settings()

    settings.load_settings_file(fixture_file("invalid.yaml"))

    assert settings.get("npc.version")

def test_loads_into_namespace():
    settings = Settings()

    settings.load_settings_file(fixture_file("valid.yaml"), namespace = "test")

    assert settings.get("test.valid") == True
