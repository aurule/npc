from click import get_app_dir
from pathlib import Path

from npc.campaign import Campaign
from npc.util import PersistentCache

class RecentCampaigns(PersistentCache):
    def __init__(self):
        super().__init__(Path(get_app_dir("NPC")) / "recent_campaigns.yml")
        self.load()

    def campaigns(self) -> list[dict]:
        return self.get("campaigns", [])

    def __bool__(self) -> bool:
        return bool(self.campaigns())

    def clear(self):
        self.data = {}
        self.save()

    def add(self, campaign: Campaign):
        new_list = self.campaigns()
        # if campaign not in list, add it to the top
        new_list.append({
            "name": campaign.name,
            "path": str(campaign.root)
            })
        self.set("campaigns", new_list[0:5])
        self.save()
