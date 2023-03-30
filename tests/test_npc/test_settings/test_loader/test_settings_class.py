import yaml

from tests.fixtures import fixture_file

from npc.settings import Settings

class TestSetup:
    def test_loads_default_settings(self):
        settings = Settings()

        assert settings.get("npc.version") != ""

    def test_loads_personal_settings(self, tmp_path):
        personal_settings = {"npc": {"editor": "custom"}}
        temp_file = tmp_path / "settings.yaml"
        temp_file.write_text(yaml.dump(personal_settings))

        settings = Settings(personal_dir = tmp_path)

        assert settings.get("npc.editor") == "custom"

    def test_saves_campaign_path(self, tmp_path):
        settings = Settings(campaign_dir = tmp_path)

        assert settings.campaign_dir == tmp_path

class TestLoadSettingsFile:
    def test_merges_valid_settings(self):
        settings = Settings()

        settings.load_settings_file(fixture_file(["valid.yaml"]))

        assert settings.get("valid") == True

    def test_ignores_missing_files(self, tmp_path):
        settings = Settings()

        settings.load_settings_file(tmp_path / "missing.yaml")

        assert settings.get("npc.version")

    def test_ignores_parse_errors(self):
        settings = Settings()

        settings.load_settings_file(fixture_file(["invalid.yaml"]))

        assert settings.get("npc.version")

class TestMergeSettings:
    def test_adds_new_values(self):
        settings = Settings()
        new_vars = {"npc": {"editor": "hello"}}

        settings.merge_settings(new_vars)

        assert settings.get("npc.editor") == "hello"

class TestGet:
    def test_returns_simple_key_value(self):
        settings = Settings()
        settings.merge_settings({"valid": True})

        result = settings.get("valid", "fail")

        assert result != "fail"

    def test_returns_nested_key_value(self):
        settings = Settings()

        result = settings.get("npc.version", "fail")

        assert result != "fail"

    def test_returns_default_with_missing_key(self):
        settings = Settings()

        result = settings.get("npc.nopealope", "missing")

        assert result == "missing"
