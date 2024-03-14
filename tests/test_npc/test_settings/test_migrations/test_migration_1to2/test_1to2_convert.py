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

def test_warns_about_legacy_templates(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    legacy_dir = tmp_campaign.root / ".npc" / "legacy"
    legacy_dir.mkdir()
    (legacy_dir / "listing").mkdir()
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore({"campaign_name": "test"})

    result = migration.convert("campaign", old_data)

    assert "Mako" in result[0].message

def test_warns_about_old_hierarchy(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    migration = Migration1to2(tmp_campaign.settings)
    old_data = DataStore({"paths": {"hierarchy": "something"}})

    result = migration.convert("campaign", old_data)

    assert "subpath_components" in result[0].message
