import pytest

from tests.fixtures import tmp_campaign

class TestWithNoCampaignDir:
    def test_returns_saved_index(self, tmp_campaign):
        assert tmp_campaign.latest_plot_index == 0
