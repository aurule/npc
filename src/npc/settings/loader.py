"""
Load and save settings info
"""

import logging
from collections import defaultdict
from importlib import resources

from pathlib import Path
from ..util import errors
from .helpers import merge_settings_dicts, prepend_namespace, quiet_parse

class Settings:
    """Core settings class

    On init, it loads the default settings, followed by settings in the personal_dir. The campaign_dir is saved
    for later use.

    Settings are stored in yaml files.
    """
    def __init__(self, personal_dir: Path = None):
        self.data: dict = {}
        if(personal_dir is None):
            personal_dir = Path('~/.config/npc/').expanduser()
        self.personal_dir: Path = personal_dir
        self.campaign_dir: Path = None

        self.install_base = resources.files("npc")
        self.default_settings_path = self.install_base / "settings"

        # load defaults and user prefs
        self.refresh()

    def refresh(self) -> None:
        """
        Clear internal data, and refresh the default and personal settings files
        """
        self.data = {}
        self.load_settings_file(self.default_settings_path / "settings.yaml")
        self.load_systems(self.default_settings_path / "systems")
        self.load_settings_file(self.personal_dir / "settings.yaml")
        self.load_systems(self.personal_dir / "systems")

    def load_campaign(self, campaign_dir: Path) -> None:
        """Load campaign settings, along with system and type configs
        
        Campaigns have a simplified directory structure compared to the primary settings paths, so this method 
        loads campaign data just a little differently.

        If campaign_dir is provided, this method will overwrite the setings object's existing value.
        
        Args:
            campaign_dir (Path): Path to the campaign settings directory to load.
        """
        self.campaign_dir = campaign_dir
        self.load_settings_file(self.campaign_dir / ".npc" / "settings.yaml")
        self.load_systems(self.campaign_dir / ".npc" / "systems")

    def load_settings_file(self, settings_file: Path, namespace: str = None) -> None:
        """Open, parse, and merge settings from another file

        This is the primary way to load more settings info. Passing in a file path that does not exist will
        result in a logged message and no error, since all setting files are optional.

        Args:
            settings_file (Path): The file to load
            namespace (str): Optional namespace to use for new_data
        """

        loaded: dict = quiet_parse(settings_file)
        if loaded is None:
            return

        self.merge_settings(loaded, namespace)

    def load_systems(self, systems_dir: Path) -> None:
        """Parse and load all system configs in systems_dir
        
        Finds all yaml files in systems_dir and loads them as systems. Special handling allows deep 
        inheritance, and prevents circular dependencies between systems.
        
        Args:
            systems_dir (Path): Dir to check for system config files
        """
        system_settings:list = systems_dir.glob("*.yaml")
        dependencies = defaultdict(list)

        for settings_file in system_settings:
            loaded = quiet_parse(settings_file)
            if loaded is None:
                continue

            system_name = list(loaded.keys())[0]
            loaded_contents = loaded[system_name]

            if "inherits" in loaded_contents:
                dependencies[loaded_contents["inherits"]].append(loaded)
                continue

            self.merge_settings(loaded, namespace="npc.systems")

        def load_dependencies(deps: dict):
            """Handle dependency loading
            
            Unrecognized parents are stored away for the next iteration. Otherwise, children are merged with 
            their parent's attributes, then merged into self.

            If the dependencies do not change for one iteration, then the remaining systems cannot be loaded 
            and are skipped.
            
            Args:
                deps (dict): Dict mapping parent system keys to child system configs
            """
            new_deps = {}
            for parent_name, children in deps.items():
                if parent_name not in self.get("npc.systems"):
                    new_deps[parent_name] = children
                    continue

                for child in children:
                    child_name = list(child.keys())[0]
                    parent_conf = dict(self.get(f"npc.systems.{parent_name}"))
                    combined = merge_settings_dicts(child[child_name], parent_conf)
                    self.merge_settings(combined, namespace=f"npc.systems.{child_name}")    
            if not new_deps:
                return
            if new_deps == deps:
                logging.error(f"Some systems could not be found: {deps.keys()}")
                return
            load_dependencies(new_deps)

        load_dependencies(dependencies)

    def merge_settings(self, new_data: dict, namespace: str = None) -> None:
        """Merge a dict of settings with this object

        Updates this object's data with the values from new_data

        Args:
            new_data (dict): Dict of settings values to merge with this object
            namespace (str): Optional namespace to use for new_data
        """
        dict_to_merge = prepend_namespace(new_data, namespace)
        self.data = merge_settings_dicts(dict_to_merge, self.data)

    def get(self, key, default=None) -> any:
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

# types
#   search paths
#   - `default/types/[system]/*.yaml`
#   - `user/types/[system]/*.yaml`
#   - `campaign/types/*.yaml`
#   sheet_path optional, defaults to type's own file dir
#       if a dir, searches as normal
#       if a file, loads file directly
#   searches for sheet file by way of typename.*, first thing that matches
#   new sheets use the found file's extension
#   expands file path on load, stores it as a Path object
