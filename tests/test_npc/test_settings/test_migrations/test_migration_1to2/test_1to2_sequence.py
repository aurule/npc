from npc.settings import Settings

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_is_first():
    settings = Settings()
    migration = Migration1to2(settings)

    assert migration.sequence is 0
