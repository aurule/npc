from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_converts_sort_by_values():
    migration = Migration1to2(Settings())
    old_data = DataStore({
        "listing": {
            "sort_by": ["last"]
        }
    })

    result = migration.convert_listing_sort(old_data)

    assert result.get("campaign.listing.sort_by")[0] == "last_name"

def test_populates_sort_by():
    migration = Migration1to2(Settings())
    old_data = DataStore({
        "listing": {
            "sort_by": ["fancy"]
        }
    })

    result = migration.convert_listing_sort(old_data)

    assert result.get("campaign.listing.sort_by")

def test_populates_group_by():
    migration = Migration1to2(Settings())
    old_data = DataStore({
        "listing": {
            "sort_by": ["pants"]
        }
    })

    result = migration.convert_listing_sort(old_data)

    assert result.get("campaign.listing.group_by")

def test_skips_missing_keys():
    migration = Migration1to2(Settings())
    old_data = DataStore()

    result = migration.convert_listing_sort(old_data)

    assert not result.get("campaign.listing.sort_by")
    assert not result.get("campaign.listing.group_by")
