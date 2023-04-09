"""
Load and save settings info
"""

import logging
import yaml
from collections import defaultdict
from importlib import resources

from pathlib import Path
from ..util import DataStore
from ..util.functions import merge_data_dicts, prepend_namespace
from .helpers import quiet_parse

class Settings(DataStore):
    """Core settings class

    On init, it loads the default settings, followed by settings in the personal_dir. The campaign_dir is saved
    for later use.

    Settings are stored in yaml files.
    """
    def __init__(self, personal_dir: Path = None):
        super().__init__()

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

        self.merge_data(loaded, namespace)

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

            self.merge_data(loaded, namespace="npc.systems")

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
                    combined = merge_data_dicts(child[child_name], parent_conf)
                    self.merge_data(combined, namespace=f"npc.systems.{child_name}")
            if not new_deps:
                return
            if new_deps == deps:
                logging.error(f"Some systems could not be found: {deps.keys()}")
                return
            load_dependencies(new_deps)

        load_dependencies(dependencies)

    @property
    def required_dirs(self) -> list:
        """Get the list of required campaign directories

        This includes the dirs for character, session, and plot files, relative to self.campaign_dir

        Returns:
            list: List of required directory names
        """
        return [
            self.get("campaign.characters.path"),
            self.get("campaign.session.path"),
            self.get("campaign.plot.path"),
        ]

    @property
    def init_dirs(self) -> list:
        """Get the list of directories to create on campaign initialization

        This includes self.required_dirs, as well as any directory listed in the settings key
        campaign.create_on_init. All paths are relative to self.campaign_dir.

        Returns:
            list: List of directory names to create on campaign init
        """
        return self.required_dirs + self.get("campaign.create_on_init")
