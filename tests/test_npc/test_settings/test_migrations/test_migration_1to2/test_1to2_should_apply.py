from npc.settings import Settings

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_true_for_old_version():
    settings = Settings()
    settings.versions["campaign"] = "1.2.3"
    migration = Migration1to2(settings)

    result = migration.should_apply("campaign")

    assert result

def test_false_for_min_version():
    settings = Settings()
    settings.versions["campaign"] = "2.0.0"
    migration = Migration1to2(settings)

    result = migration.should_apply("campaign")

    assert not result

def test_false_for_future_version():
    settings = Settings()
    settings.versions["campaign"] = "2.3.4"
    migration = Migration1to2(settings)

    result = migration.should_apply("campaign")

    assert not result
