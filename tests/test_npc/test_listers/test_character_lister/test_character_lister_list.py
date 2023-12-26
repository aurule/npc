import pytest
from io import StringIO
from tests.fixtures import fixture_file, ProgressCounter, db
from npc.campaign import Campaign

from npc.listers import CharacterLister

class TestCharacters:
    def test_includes_names(self, db):
        campaign = Campaign(fixture_file("listing", "show_all"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "Test Mann" in result
        assert "Frank" in result

    def test_excludes_delist(self, db):
        campaign = Campaign(fixture_file("listing", "skip_delist"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "Test Mann" in result
        assert "Frank" not in result

    def test_char_header_higher_than_groups(self, db):
        campaign = Campaign(fixture_file("listing", "basic_groups"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# M" in result
        assert "## Test Mann" in result

class TestGroupings:
    def test_group_header_levels_increment(self, db):
        campaign = Campaign(fixture_file("listing", "basic_groups"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# M" in result
        assert "## T" in result
        assert "### Test Mann" in result

    def test_resets_subgroups(self, db):
        campaign = Campaign(fixture_file("listing", "basic_groups"))
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

    def test_labels_null_group_static(self, db):
        campaign = Campaign(fixture_file("listing", "missing_groups"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "# No org" in result

class TestFilters():
    def test_renders_markdown(self, db):
        campaign = Campaign(fixture_file("listing", "markdown"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="html")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "<p>A <em>testing</em> string with <strong>markdown</strong></p>" in result

    def test_renders_inline_markdown(self, db):
        campaign = Campaign(fixture_file("listing", "markdown"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="html")
        target = StringIO()

        lister.list(target=target)

        result = target.getvalue()
        assert "<span>A <em>testing</em> string with <strong>markdown</strong></span>" in result

class TestProgressBar():
    def test_updates_progress(self, db):
        campaign = Campaign(fixture_file("listing", "show_all"))
        campaign.characters.db = db
        campaign.characters.refresh()
        lister = CharacterLister(campaign.characters, lang="markdown")
        target = StringIO()
        counter = ProgressCounter()

        lister.list(target=target, progress_callback=counter.progress)

        assert counter.count == 2
