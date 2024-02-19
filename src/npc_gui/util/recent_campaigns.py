from click import get_app_dir
from pathlib import Path

from npc.campaign import Campaign
from npc.util import PersistentCache

class RecentCampaigns(PersistentCache):
    """Helper class to maintain a list of recently opened campaigns

    This class maintains a yaml file with recent campaign info. Use the add
    method whenever a campaign is opened, and the campaigns method to get the
    list of recent campaign data. The campaign list is ordered from oldest to
    newest.

    Attributes:
        MAX_RECENTS: Maximum number of saved campaigns.
    """

    MAX_RECENTS = 5

    def __init__(self, cache_path: str = None):
        if cache_path:
            file_path = Path(cache_path)
        else:
            file_path = Path(get_app_dir("NPC")) / "recent_campaigns.yml"
        super().__init__(file_path)
        self.load()

    def campaigns(self) -> list[dict]:
        """Get a list of all recent campaigns

        Each item is a dict with a name and path value.

        Returns:
            list[dict]: List of recent campaign info.
        """
        return self.get("campaigns", [])

    def __bool__(self) -> bool:
        """Convert this cache to a boolean value

        A recent campaigns object is considered True if it has one or more
        saved campaigns, and False if not.

        Returns:
            bool: True if there are saved campaigns, False if not
        """
        return bool(self.campaigns())

    def add(self, campaign: Campaign):
        """Add a recent campaign to the list

        The given campaign is always added to the end of the list. If its path
        already exists, the old entry will be removed. This means that the name
        will be updated.

        Args:
            campaign (Campaign): The campaign to add
        """
        new_list = [c for c in self.campaigns() if c["path"] != str(campaign.root)]
        new_list.append({
            "name": campaign.name,
            "path": str(campaign.root)
            })
        self.set("campaigns", new_list[-self.__class__.MAX_RECENTS:])
        self.save()
