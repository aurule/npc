import json
import yaml
from npc.campaign import Campaign

from npc.settings.migrations.migration_1to2 import Migration1to2

def prep_legacy_json(root):
    settings_dir = root.joinpath(".npc")
    settings_dir.mkdir(exist_ok=True)
    legacy_file = settings_dir.joinpath("settings.json")
    legacy_data = {"legacy": "json"}
    with legacy_file.open("w") as f:
        json.dump(legacy_data, f)

def prep_legacy_yaml(root):
    settings_dir = root.joinpath(".npc")
    settings_dir.mkdir(exist_ok=True)
    legacy_file = settings_dir.joinpath("settings.yml")
    legacy_data = {"legacy": "yaml"}
    with legacy_file.open("w") as f:
        yaml.dump(legacy_data, f)

def test_loads_json(tmp_path):
    prep_legacy_json(tmp_path)
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    data = migration.load_legacy("campaign")

    assert data.get("legacy") == "json"

def test_loads_yml(tmp_path):
    prep_legacy_yaml(tmp_path)
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    data = migration.load_legacy("campaign")

    assert data.get("legacy") == "yaml"

def test_prefers_json(tmp_path):
    prep_legacy_json(tmp_path)
    prep_legacy_yaml(tmp_path)
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    data = migration.load_legacy("campaign")

    assert data.get("legacy") == "json"

def test_returns_empty_store_with_no_legacy_file(tmp_path):
    campaign = Campaign(tmp_path)
    migration = Migration1to2(campaign.settings)

    data = migration.load_legacy("campaign")

    assert not data
