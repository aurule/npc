import pytest
from tests.fixtures import fixture_file
from npc.util import ParseError

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

def test_throws_parse_error_on_missing_def():
    settings = Settings()

    with pytest.raises(ParseError):
        settings.load_types(
            fixture_file("campaigns", "empty_type", ".npc", "types"),
            system_key = "generic")

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
        system_key = "fate-venture")

    assert "nameless" in settings.get("npc.types.fate-venture")

def test_overrides_inherited_types():
    settings = Settings()

    settings.load_types(
        fixture_file("campaigns", "types_inherit", ".npc", "types"),
        system_key = "fate-venture",
        namespace_root = "campaign")

    assert "Testier" == settings.get("campaign.types.fate-venture.test.name")

class TestResolvesExplicitSheetPath():
    def test_resolves_absolute_path(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "pet",
            namespace_root = "campaign")

        assert ".." not in str(settings.get("campaign.types.pet.dog.sheet_path"))

    def test_expands_relative_path_from_typedef(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "other",
            namespace_root = "campaign")

        assert "sessile" in str(settings.get("campaign.types.other.tree.sheet_path"))

    def test_stores_real_path(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "other",
            namespace_root = "campaign")

        assert settings.get("campaign.types.other.tree.sheet_path").exists()

class TestInsertsImplicitSheetPaths():
    def test_assigns_discovered_files_using_stem(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "generic",
            namespace_root = "campaign")

        assert "animal" in str(settings.get("campaign.types.generic.animal.sheet_path"))

    def test_skips_undefined_types(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "generic",
            namespace_root = "campaign")

        assert "foobar" not in settings.get("campaign.types.generic")

    def test_skips_existing_sheet_paths(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "generic",
            namespace_root = "campaign")

        assert "animal" in str(settings.get("campaign.types.generic.useconf.sheet_path"))

    def test_stores_real_path(self):
        settings = Settings()

        settings.load_types(
            fixture_file("campaigns", "sheets", ".npc", "types"),
            system_key = "generic",
            namespace_root = "campaign")

        assert settings.get("campaign.types.generic.animal.sheet_path").exists()
