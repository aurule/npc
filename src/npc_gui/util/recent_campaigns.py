from click import get_app_dir
from pathlib import Path

from npc.util import PersistentCache

class RecentCampaigns(PersistentCache):
    def __init__(self):
        super().__init__(Path(get_app_dir("NPC")) / "recent_campaigns.yml")
        self.load()

    def campaigns(self) -> list[dict]:
        return self.get("campaigns", [])
