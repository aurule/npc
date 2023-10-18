import pytest

from tests.fixtures import tmp_campaign, change_cwd, MockSettings

from npc_cli.helpers import campaign_or_fail
from npc_cli.errors import CampaignNotFoundException

def test_raises_on_missing_campaign(tmp_path):
    settings = MockSettings()
    with change_cwd(tmp_path):
        with pytest.raises(CampaignNotFoundException):
            campaign_or_fail(settings)

def test_returns_campaign_for_current_dir(tmp_campaign):
    settings = MockSettings()
    with change_cwd(tmp_campaign.root):
        campaign = campaign_or_fail(settings)

        assert campaign.root == tmp_campaign.root

def test_returns_campaign_for_parent_dir(tmp_campaign):
    settings = MockSettings()

    with change_cwd(tmp_campaign.root / "Plot"):
        campaign = campaign_or_fail(settings)

        assert campaign.root == tmp_campaign.root
