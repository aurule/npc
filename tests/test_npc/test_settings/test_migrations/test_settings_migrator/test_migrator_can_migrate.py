from tests.fixtures import MockMigration, MockSettings

from npc.settings.migrations import SettingsMigrator

def test_true_with_migrations():
    settings = MockSettings()
    settings.versions["test"] = "1.2.3"
    migrator = SettingsMigrator(settings)

    result = migrator.can_migrate("test")

    assert result

def test_false_without_migrations():
    settings = MockSettings()
    migrator = SettingsMigrator(settings)

    result = migrator.can_migrate("internal")

    assert not result
