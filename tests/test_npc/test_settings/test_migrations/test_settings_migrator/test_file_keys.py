from tests.fixtures import MockSettings

from npc.settings.migrations import SettingsMigrator

def test_gets_keys_with_paths():
    settings = MockSettings()
    settings.loaded_paths["test"] = "something/fake"
    migrator = SettingsMigrator(settings)

    keys = migrator.file_keys

    assert "test" in keys

def test_ignores_keys_without_paths():
    settings = MockSettings()
    settings.versions["test"] = "1.2.3"
    migrator = SettingsMigrator(settings)

    keys = migrator.file_keys

    assert "test" not in keys

def test_skips_package():
    settings = MockSettings()
    migrator = SettingsMigrator(settings)

    keys = migrator.file_keys

    assert "package" not in keys

def test_skips_internal():
    settings = MockSettings()
    migrator = SettingsMigrator(settings)

    keys = migrator.file_keys

    assert "internal" not in keys
