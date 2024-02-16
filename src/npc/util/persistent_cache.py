import yaml
from pathlib import Path

from .data_store import DataStore
from .functions import parse_yaml

class PersistentCache(DataStore):
    """Class for storing and retrieving long-term data

    This class does not load from its file immediately.
    """
    def __init__(self, file_path: Path, data_in = None):
        super().__init__(data_in)

        self.cache_file_path = file_path

    def load(self):
        """Open the cache file and load its contents

        This method will completely replace the current data with the contents
        of the cache file.
        """
        self.data = {}

        if not self.cache_file_path.exists():
            return

        loaded: dict = parse_yaml(self.cache_file_path)
        self.merge_data(loaded)

    def save(self):
        """Write our data to the cache file

        This overwrites the contents entirely.
        """
        with self.cache_file_path.open("w", newline="\n") as cache_file:
            yaml.dump(self.data, cache_file, default_flow_style=False)
