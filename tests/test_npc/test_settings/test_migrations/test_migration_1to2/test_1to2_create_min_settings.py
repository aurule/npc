from npc.campaign import Campaign

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_populates_file(tmp_path):
    tmp_path.joinpath(".npc").mkdir()
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    migration.create_min_settings("campaign")

    assert campaign.settings_file.exists()

def test_sets_version(tmp_path):
    tmp_path.joinpath(".npc").mkdir()
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    migration.create_min_settings("campaign")

    data = migration.load_yaml("campaign")
    assert data.get("npc.version") == "2.0.0"
