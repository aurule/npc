from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_converts_existing_keys():
    migration = Migration1to2(Settings())
    old_data = DataStore({
        "editor": "just a test"
    })

    result = migration.convert_legacy_keys(old_data)

    assert result.get("npc.editor") == "just a test"

def test_skips_missing_keys():
    migration = Migration1to2(Settings())
    old_data = DataStore({
        "fleditor": "just a test"
    })

    result = migration.convert_legacy_keys(old_data)

    assert result.get("npc.editor") is None
