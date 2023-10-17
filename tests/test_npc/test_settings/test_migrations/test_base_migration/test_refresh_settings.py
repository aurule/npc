import pytest
from tests.fixtures import tmp_campaign, FakeMigration

def test_adds_new_keys(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    data = {"npc": {"test": "very yes"}}
    migration.write_settings("campaign", data)

    migration.refresh_settings("campaign")

    assert migration.settings.get("npc.test") == "very yes"
