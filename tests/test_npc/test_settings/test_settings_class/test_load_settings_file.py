from tests.fixtures import fixture_file, MockSettings

from npc.settings import Settings

def test_loads_valid_Mocksettings():
    settings = MockSettings()

    settings.load_settings_file(fixture_file("yaml", "valid.yaml"))

    assert settings.get("valid") == True

def test_ignores_missing_files(tmp_path):
    settings = MockSettings()

    settings.load_settings_file(tmp_path / "missing.yaml")

    assert settings.get("npc.tags")

def test_ignores_parse_errors():
    settings = MockSettings()

    settings.load_settings_file(fixture_file("yaml", "invalid.yaml"))

    assert settings.get("npc.tags")

def test_loads_into_namespace():
    settings = MockSettings()

    settings.load_settings_file(fixture_file("yaml", "valid.yaml"), namespace = "test")

    assert settings.get("test.valid") == True

class TestVersionHandling():
    def test_without_file_key_does_not_store(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "with_version.yaml"))

        result = settings.get("npc.version")
        assert result
        assert result not in settings.versions

    def test_with_version_stores_in_key(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "with_version.yaml"), file_key="test")

        assert settings.versions.get("test") == "2.3.4-test"

    def test_without_version_stores_none(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "no_version.yaml"), file_key="test")

        assert settings.versions.get("test", "error!") is None

    def test_removes_version_from_data(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "with_version.yaml"), file_key="test")

        assert settings.get("npc.version") is None

    def test_without_file_and_json_fallback_stores_placeholder(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "json_fallback", "missing.yaml"), file_key="test")

        assert settings.versions.get("test") == "1.0.0"

    def test_without_file_and_yml_fallback_stores_placeholder(self):
        settings = MockSettings()

        settings.load_settings_file(fixture_file("settings", "yml_fallback", "missing.yaml"), file_key="test")

        assert settings.versions.get("test") == "1.0.0"

class TestPathHandling():
    def test_without_file_key_does_not_store_blank(self):
        settings = MockSettings()
        file_path = fixture_file("settings", "with_version.yaml")

        settings.load_settings_file(file_path)

        assert file_path not in settings.loaded_paths

    def test_with_version_stores_path(self):
        settings = MockSettings()
        file_path = fixture_file("settings", "with_version.yaml")

        settings.load_settings_file(file_path, file_key="test")

        assert settings.loaded_paths.get("test") == file_path
