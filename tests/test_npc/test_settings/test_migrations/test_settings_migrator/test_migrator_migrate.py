from npc.settings import Settings
from tests.fixtures import MockMigration

from npc.settings.migrations import SettingsMigrator

def test_executes_migrations(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")

    settings = Settings()
    settings.load_settings_file(settings_file, file_key="test")
    migrator = SettingsMigrator(settings)

    migrator.migrate("test")

    settings.load_settings_file(settings_file, file_key="test")
    assert settings.get("npc.tested")

def test_returns_messages(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")

    settings = Settings()
    settings.load_settings_file(settings_file, file_key="test")
    migrator = SettingsMigrator(settings)

    messages = migrator.migrate("test")

    assert messages[0]
