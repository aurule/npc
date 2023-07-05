import pytest
from io import StringIO
from tests.fixtures import fixture_file
from npc.db import DB
from npc.campaign import Campaign

from npc.listers import CharacterLister

class TestCharacters:
    def test_includes_names(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "show_all"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "Test Mann" in result
        assert "Frank" in result

    def test_excludes_delist(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "skip_delist"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "Test Mann" in result
        assert "Frank" not in result

    def test_char_header_higher_than_groups(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "basic_groups"))
        campaign.patch_campaign_settings({"characters": {"listing": {"group_by": ["last_initial"]}}})
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# M" in result
        assert "## Test Mann" in result

class TestGroupings:
    def test_group_header_levels_increment(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "basic_groups"))
        campaign.patch_campaign_settings({"characters": {"listing": {"group_by": ["last_initial", "first_initial"]}}})
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# M" in result
        assert "## T" in result
        assert "### Test Mann" in result

    def test_resets_subgroups(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "basic_groups"))
        campaign.patch_campaign_settings({"characters": {"listing": {"group_by": ["last_initial", "first_initial"]}}})
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# F" in result
        assert "## F" in result
        assert "### Frank" in result
        assert "# M" in result
        assert "## T" in result
        assert "### Test Mann" in result

    @pytest.mark.xfail(reason="query builder excludes characters without named tag")
    def test_labels_null_group_static(self):
        db = DB(clearSingleton=True)
        campaign = Campaign(fixture_file("listing", "missing_groups"))
        campaign.patch_campaign_settings({"characters": {"listing": {"group_by": ["org"]}}})
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "No Org" in result
