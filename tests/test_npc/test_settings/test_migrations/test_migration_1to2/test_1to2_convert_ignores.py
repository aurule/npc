from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_skips_on_no_campaign():
    settings = Settings()
    migration = Migration1to2(settings)
    old_data = DataStore()

    new_data = migration.convert_ignores(old_data)

    assert not new_data.get("campaign.characters.ignore_subpaths")

def test_skips_on_no_global_ignores(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore()

    new_data = migration.convert_ignores(old_data)

    assert not new_data.get("campaign.characters.ignore_subpaths")

def test_adds_ignores(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore({
        "paths": {
            "ignore": {
                "always": {
                    "Characters/Deceased"
                }
            }
        }
    })

    new_data = migration.convert_ignores(old_data)

    assert new_data.get("campaign.characters.ignore_subpaths") == ['Deceased']
