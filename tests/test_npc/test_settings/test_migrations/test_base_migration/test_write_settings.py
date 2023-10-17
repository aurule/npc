from tests.fixtures import tmp_campaign, FakeMigration
from npc.util import DataStore

def test_creates_file(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    migration = FakeMigration(tmp_campaign.settings)

    migration.write_settings("campaign", {"testing": "very yes"})

    data = migration.load_settings("campaign")
    assert data.get("testing") == "very yes"

def test_overwrites_file(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)

    migration.write_settings("campaign", {"testing": "very yes"})

    data = migration.load_settings("campaign")
    assert data.get("testing") == "very yes"

def test_accepts_datastore(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    data = DataStore({"testing": "very yes"})

    migration.write_settings("campaign", data)

    data = migration.load_settings("campaign")
    assert data.get("testing") == "very yes"
