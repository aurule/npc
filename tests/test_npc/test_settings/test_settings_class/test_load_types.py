from tests.fixtures import fixture_file

from npc.settings import Settings

def test_loads_universal_types():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "chonk", ".npc", "types"),
        system_key = "generic")

    assert "pet" in settings.get("npc.types.generic")

def test_loads_system_dir_types():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "chungus", ".npc", "types"),
        system_key = "generic")

    assert "plant" in settings.get("npc.types.generic")

def test_ignores_types_from_other_systems():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "chungus", ".npc", "types"),
        system_key = "generic")

    assert "tree" not in settings.get("npc.types.generic")

def test_loads_into_given_namespace():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "chungus", ".npc", "types"),
        system_key = "generic",
        namespace_root = "campaign")

    assert "pet" in settings.get("campaign.types.generic")

def test_defaults_to_npc_namespace():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "chungus", ".npc", "types"),
        system_key = "generic")

    assert "pet" in settings.get("npc.types.generic")

def test_loads_inherited_system_types():
    settings = Settings()

    settings.load_types(
        settings.default_settings_path / "types",
        system_key = "fate-ep")

    assert "nameless" in settings.get("npc.types.fate-ep")

def test_overrides_inherited_types():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "types_inherit", ".npc", "types"),
        system_key = "fate-ep",
        namespace_root = "campaign")

    assert "Testier" == settings.get("campaign.types.fate-ep.test.name")
