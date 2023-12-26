from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_skips_missing_key(tmp_campaign):
    tmp_campaign.settings_dir.joinpath("legacy").mkdir()
    old_file = tmp_campaign.settings_dir / "legacy" / "Test.haha"
    with old_file.open('w', newline="\n") as f:
        f.write("a simple test sheet")
    old_data = DataStore({
        "types": {
            "test": {
                "nah": "yah"
            }
        }
    })
    migration = Migration1to2(tmp_campaign.settings)

    migration.convert_type_templates("campaign", old_data)

    new_file = tmp_campaign.settings_dir / "types" / "test.haha"
    assert not new_file.exists()

def test_skips_missing_file(tmp_campaign):
    tmp_campaign.settings_dir.joinpath("legacy").mkdir()
    old_data = DataStore({
        "types": {
            "test": {
                "sheet_template": "Test.nope"
            }
        }
    })
    migration = Migration1to2(tmp_campaign.settings)

    migration.convert_type_templates("campaign", old_data)

    new_file = tmp_campaign.settings_dir / "types" / "test.nope"
    assert not new_file.exists()

def test_keeps_old_suffix(tmp_campaign):
    tmp_campaign.settings_dir.joinpath("legacy").mkdir()
    old_file = tmp_campaign.settings_dir / "legacy" / "Test.farkle"
    with old_file.open('w', newline="\n") as f:
        f.write("a simple test sheet")
    old_data = DataStore({
        "types": {
            "test": {
                "sheet_template": "Test.farkle"
            }
        }
    })
    migration = Migration1to2(tmp_campaign.settings)

    migration.convert_type_templates("campaign", old_data)

    new_file = tmp_campaign.settings_dir / "types" / "test.farkle"
    assert new_file.exists()

def test_copies_contents(tmp_campaign):
    tmp_campaign.settings_dir.joinpath("legacy").mkdir()
    old_file = tmp_campaign.settings_dir / "legacy" / "Test.npc"
    with old_file.open('w', newline="\n") as f:
        f.write("a simple test sheet")
    old_data = DataStore({
        "types": {
            "test": {
                "sheet_template": "Test.npc"
            }
        }
    })
    migration = Migration1to2(tmp_campaign.settings)

    migration.convert_type_templates("campaign", old_data)

    new_file = tmp_campaign.settings_dir / "types" / "test.npc"
    with new_file.open('r') as f:
        contents = f.read()

    assert contents == "a simple test sheet"

def test_renames_to_type_key(tmp_campaign):
    tmp_campaign.settings_dir.joinpath("legacy").mkdir()
    old_file = tmp_campaign.settings_dir / "legacy" / "Test.npc"
    with old_file.open('w', newline="\n") as f:
        f.write("a simple test sheet")
    old_data = DataStore({
        "types": {
            "test": {
                "sheet_template": "Test.npc"
            }
        }
    })
    migration = Migration1to2(tmp_campaign.settings)

    migration.convert_type_templates("campaign", old_data)

    new_file = tmp_campaign.settings_dir / "types" / "test.npc"
    assert new_file.exists()
