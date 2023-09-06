from tests.fixtures import tmp_campaign

from npc.settings import Settings

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_false_on_missing_file(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    migration = Migration1to2(tmp_campaign.settings)

    assert not migration.modern_format("campaign")

def test_false_on_missing_keys(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)
    migration.write_settings("campaign", {"nope": "alope"})

    assert not migration.modern_format("campaign")

def test_true_on_valid_keys(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)

    assert migration.modern_format("campaign")
