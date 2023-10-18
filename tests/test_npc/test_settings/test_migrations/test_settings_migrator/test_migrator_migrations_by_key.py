from tests.fixtures import MockMigration, MockSettings

from npc.settings.migrations import SettingsMigrator

def test_includes_applicable_migrations(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")
    other_file = tmp_path / "other.yaml"
    with settings_file.open("w") as f:
        f.write("other: {tested: false, version: 2.0.0}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    settings.load_settings_file(other_file, file_key="nope")
    migrator = SettingsMigrator(settings)

    migrations = migrator.migrations_by_file_key()

    assert migrations.get("test")

def test_excludes_non_applicable_migrations(tmp_path):
    settings_file = tmp_path / "settings.yaml"
    with settings_file.open("w") as f:
        f.write("npc: {tested: false, version: 2.0.0}")
    other_file = tmp_path / "other.yaml"
    with settings_file.open("w") as f:
        f.write("other: {tested: false, version: 2.0.0}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    settings.load_settings_file(other_file, file_key="nope")
    migrator = SettingsMigrator(settings)

    migrations = migrator.migrations_by_file_key()

    assert not migrations.get("nope")
