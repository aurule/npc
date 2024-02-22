from pathlib import Path
from ruamel.yaml import YAML

from npc.util import DataStore

class SettingsWriter(DataStore):
    """Perform non-destructive round-trip editing of a yaml file

    This class is meant to load, modify data, then write a single yaml file. It uses the ruamel.yaml parser
    in order to preserve the file's existing formatting and comments, at the cost of slower speed.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.yaml = YAML(typ="rt")
        self.yaml.default_flow_style = False

    def load(self):
        """Read data from the file

        Loads the file's data. Unlike other DataStore subclasses, the internal data is entirely replaced using
        a dict-like object from the parser which encodes formatting, comments, etc.
        """
        self.data = self.yaml.load(self.file_path)

    def save(self):
        """Write our data to the file
        """
        self.yaml.dump(self.data, self.file_path)

    def merge_data(self, *args, **kwargs):
        """DISABLED: Merge a dict of data into our own data

        This standard method on the DataStore class is disabled. Since we use a special object from the parser
        instead of a normal dict, the default implementation of merge_data would destroy the context info that
        we want to preserve.

        Throws:
            NotImplementedError whenever called
        """
        raise NotImplementedError
