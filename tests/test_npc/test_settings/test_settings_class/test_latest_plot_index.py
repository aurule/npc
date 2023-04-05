import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

class TestWithNoCampaignDir:
    def test_returns_saved_index(self):
        settings = Settings()

        assert settings.latest_plot_index == 0
