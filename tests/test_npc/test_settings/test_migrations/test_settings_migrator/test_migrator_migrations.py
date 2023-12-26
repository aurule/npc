from tests.fixtures import MockMigration, MockSettings

from npc.settings.migrations import SettingsMigrator

def test_gets_all_migrations():
    settings = MockSettings()
    migrator = SettingsMigrator(settings)

    migrations = migrator.migrations

    assert len(migrations)

def test_sorts_migrations():
    settings = MockSettings()
    migrator = SettingsMigrator(settings)

    migrations = migrator.migrations

    first_seq = migrations[0].sequence
    last_seq = migrations[-1].sequence
    assert first_seq < last_seq
