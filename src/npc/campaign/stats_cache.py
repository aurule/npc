from pathlib import Path

from npc.util import PersistentCache

class StatsCache(PersistentCache):
    def __init__(self, campaign: "Campaign"):
        file_path = campaign.cache_dir / "stats.yaml"
        super().__init__(file_path)
        self.load()

    def set(self, key: str, value: any):
        """Write a value to a key and immediately save

        Identical to DataStore.set, with the addition of immediately writing our data to our file.

        Args:
            key (str): Period-delimited key to set
            value (any): New value for the final member of the key

        Raises:
            TypeError: Raised when accessing a list
        """
        super().set(key, value)
        self.save()
