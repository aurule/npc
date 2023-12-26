from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_adds_version(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore()

    migration.convert("campaign", old_data)

    new_data = migration.load_settings("campaign")
    assert new_data.get("npc.version")

def test_converts_keys(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore({"campaign_name": "test"})

    migration.convert("campaign", old_data)

    new_data = migration.load_settings("campaign")
    assert new_data.get("campaign.name") == "test"
