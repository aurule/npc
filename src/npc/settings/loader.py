"""
Load and save settings info
"""

import logging
import yaml

from pathlib import Path
from ..util import errors, parse_yaml
from .helpers import merge_settings_dicts

# file loading
# * use .yaml and .yml
# * each successive file merges or overwrites keys with the same path
#     - lists are merged
#     - dicts are merged
#     - other values are overwritten
# * location search order
#     - internal
#     - user home
#     - campaign
# * file load order
#     - `settings.yaml`
#     - campaign.system
# * special handling
#     - systems can `inherit` from another system. Before merging the target system, check its `inherits` property and load that system first. Then finish merging the target system.
# * lazy load `system/type/*.yaml` individually or singly as required

class Settings:
    def __init__(self, personal_dir: Path = None, campaign_dir: Path = None, verbose: bool = False):
        self.data: dict = {}
        self.verbose: bool = verbose
        if(personal_dir is None):
            personal_dir = Path('~/.config/npc/').expanduser()
        self.personal_dir: Path = personal_dir
        self.campaign_dir: Path = campaign_dir

        self.default_settings_path: Path = Path(__file__).parent
        self.install_base: Path = Path(self.default_settings_path).parent

        # load defaults and user prefs
        self.load_settings(self.install_base)
        self.load_settings(self.personal_dir)

    def load_settings(self, settings_dir: Path) -> None:
        settings_file = settings_dir / 'settings.yaml'
        if not settings_file.exists():
            settings_file = settings_dir / 'settings.yml'

        try:
            self.load_settings_file(settings_file)
        except OSError as err:
            # Settings are optional, so we silently ignore these errors
            logging.info('Missing settings file %s', settings_file)

    def load_settings_file(self, settings_file: Path) -> None:
        try:
            loaded = parse_yaml(settings_file)
        except util.errors.ParseError as err:
            logging.warn(err.strerror)
            return

        self.merge_settings(loaded)

    def merge_settings(self, new_data: dict) -> None:
        self.data = merge_settings_dicts(new_data, self.data)
