from click import get_app_dir
from pathlib import Path

from npc.campaign import Campaign
from npc.util import PersistentCache

class RecentCampaigns(PersistentCache):

    MAX_RECENTS = 5

    def __init__(self, cache_path: str = None):
        if cache_path:
            file_path = Path(cache_path)
        else:
            file_path = Path(get_app_dir("NPC")) / "recent_campaigns.yml"
        super().__init__(file_path)
        self.load()

    def campaigns(self) -> list[dict]:
        return self.get("campaigns", [])

    def __bool__(self) -> bool:
        return bool(self.campaigns())

    def add(self, campaign: Campaign):
        new_list = [c for c in self.campaigns() if c["path"] != str(campaign.root)]
        new_list.append({
            "name": campaign.name,
            "path": str(campaign.root)
            })
        self.set("campaigns", new_list[-self.__class__.MAX_RECENTS:])
        self.save()
