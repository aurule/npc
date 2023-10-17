from tests.fixtures import tmp_campaign, FakeMigration

def test_overwrites_version(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)

    migration.update_version("campaign", "2.3.4")

    data = migration.load_settings("campaign")
    assert data.get("npc.version") == "2.3.4"
