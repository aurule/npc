from tests.fixtures import tmp_campaign, change_cwd
from npc.settings import Settings

from npc_cli.helpers import get_campaign

def test_aborts_on_missing_campaign(tmp_path):
    settings = Settings()
    with change_cwd(tmp_path):
        campaign = get_campaign(settings)

        assert campaign is None

def test_returns_campaign_for_current_dir(tmp_campaign):
    settings = Settings()
    with change_cwd(tmp_campaign.root):
        campaign = get_campaign(settings)

        assert campaign.root == tmp_campaign.root

def test_returns_campaign_for_parent_dir(tmp_campaign):
    settings = Settings()

    with change_cwd(tmp_campaign.root / "Plot"):
        campaign = get_campaign(settings)

        assert campaign.root == tmp_campaign.root
