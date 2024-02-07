from tests.fixtures import MockSettings

from npc.settings.migrations import SettingsMigrator

def test_executes_all_migrations(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    migrator = SettingsMigrator(settings)

    migrator.migrate_all()

    settings.load_settings_file(settings_file, file_key="test")
    assert settings.get("npc.tested")

def test_returns_all_messages(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    migrator = SettingsMigrator(settings)

    messages = migrator.migrate_all()

    assert messages[0]
