from .. import Settings
from npc.util import DataStore
from npc.util.errors import

class GameSystem(DataStore):
    """Represents data about a specific game system

    Loads and compiles system data from a setings object, and makes it easy to use
    """
    def __init__(self, settings: Settings, system_key: str):
        super().__init__()

        self.merge_data(settings.get(f"npc.systems.{system_key}", {}))
        self.merge_data(settings.get(f"npc.campaign.systems.{system_key}", {}))

        self.name = self.get("name")
        self.desc = self.get("desc")

        # desired properties:
        # self.tags_hash
        # self.tags
        # self.deprecated_tags
        # self.meta_tags
        # self.types
