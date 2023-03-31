"""
Load and save settings info
"""

import logging
import yaml

from pathlib import Path
from ..util import errors, parse_yaml
from .helpers import merge_settings_dicts

"""Core settings class

On init, it loads the default settings, followed by settings in the personal_dir. The campaign_dir is saved
for later use.

Settings are stored in yaml files.
"""
class Settings:
    def __init__(self, personal_dir: Path = None, campaign_dir: Path = None):
        self.data: dict = {}
        if(personal_dir is None):
            personal_dir = Path('~/.config/npc/').expanduser()
        self.personal_dir: Path = personal_dir
        self.campaign_dir: Path = campaign_dir

        self.default_settings_path: Path = Path(__file__).parent
        self.install_base: Path = Path(self.default_settings_path).parent

        # load defaults and user prefs
        self.refresh()

    def refresh(self):
        """
        Clear internal data, and refresh the default and personal settings files
        """
        self.data = {}
        self.load_settings_file(self.install_base / "settings" / "settings.yaml")
        self.load_settings_file(self.personal_dir / "settings.yaml")

    def load_settings_file(self, settings_file: Path) -> None:
        """Open, parse, and merge settings from another file

        This is the primary way to load more settings info. Passing in a file path that does not exist will
        result in a logged message and no error, since all setting files are optional.

        Args:
            settings_file (Path): The file to load
        """

        try:
            loaded = parse_yaml(settings_file)
        except OSError as err:
            # Settings are optional, so we silently ignore these errors
            logging.info('Missing settings file %s', settings_file)
            return
        except errors.ParseError as err:
            logging.warning(err.strerror)
            return

        self.merge_settings(loaded)

    def merge_settings(self, new_data: dict) -> None:
        """Merge a dict of settings with this object

        Updates this object's data with the values from new_data

        Args:
            new_data (dict): Dict of settings values to merge with this object
        """
        self.data = merge_settings_dicts(new_data, self.data)

    def get(self, key, default=None):
        """
        Get the value of a settings key

        Use the period character to indicate a nested key. So, the key
        "alpha.beta.charlie" is looked up like
        `data['alpha']['beta']['charlie']`.

        Args:
            key (str): Key to get from settings.
            default (any): Value to return when key isn't found.

        Returns:
            The value in that key, or None if the key could not be resolved.
        """
        key_parts: list = key.split('.')
        current_data = self.data
        for k in key_parts:
            try:
                current_data = current_data[k]
            except (KeyError, TypeError):
                logging.debug("Key not found: {}".format(key))
                return default
        return current_data

    # systems
    #   lazy load on request
    #   can `inherit` from another system
    #       Before merging the target system, check its `inherits` property and load that system first. Then finish merging the target system.
    # types
    #   lazy load on request
