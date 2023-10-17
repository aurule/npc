from npc.settings import Settings
from tests.fixtures import MockMigration

from npc.settings.migrations import SettingsMigrator

def test_true_with_migrations():
    settings = Settings()
    settings.versions["test"] = "1.2.3"
    migrator = SettingsMigrator(settings)

    result = migrator.can_migrate("test")

    assert result

def test_false_without_migrations():
    settings = Settings()
    migrator = SettingsMigrator(settings)

    result = migrator.can_migrate("internal")

    assert not result
