from tests.fixtures import fixture_file

from npc.campaign import find_campaign_root

class TestWithCampaignDir:
    def test_returns_curent_dir(self):
        campaign_dir = fixture_file("campaigns", "find_root")

        result = find_campaign_root(campaign_dir)

        assert result == campaign_dir

class TestWithInsideDir:
    def test_returns_parent_dir(self):
        campaign_dir = fixture_file("campaigns", "find_root")

        result = find_campaign_root(campaign_dir / "deep" / "nesting")

        assert result == campaign_dir

class TestWithBadDir:
    def test_returns_none(self, tmp_path):
        result = find_campaign_root(tmp_path)

        assert result is None
