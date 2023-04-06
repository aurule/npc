"""
Load and save settings info
"""

import logging
import re
import yaml
from collections import defaultdict
from importlib import resources

from pathlib import Path
from ..util import errors
from .helpers import merge_settings_dicts, prepend_namespace, quiet_parse
from .planning_filename import PlanningFilename

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
        self.load_settings_file(self.campaign_settings_file)
        self.load_systems(self.campaign_settings_dir / "systems")

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

    @property
    def campaign_settings_dir(self) -> Path:
        """Get the path to the current campaign settings directory

        Returns:
            Path: Path to the campaign's settings dir, or None if campaign_dir is not set
        """
        if not self.campaign_dir:
            return None

        return self.campaign_dir / ".npc"

    @property
    def campaign_settings_file(self) -> Path:
        """Get the path to the current campaign settings file

        Returns:
            Path: Path to the campaign's settings file, or None if campaign_dir is not set
        """
        if not self.campaign_dir:
            return None

        return self.campaign_settings_dir / "settings.yaml"

    def patch_campaign_settings(self, data: dict) -> None:
        """Update some values in the campaign settings and corresponding file

        Updates the internal campaign settings with data, then writes those changes to the current campaign's
        settings file.

        If campaign_dir is not set, this returns immediately.

        Args:
            data (dict): Data to change
        """
        if not self.campaign_dir:
            return

        new_data = prepend_namespace(data, "campaign")
        self.merge_settings(new_data)

        settings_file = self.campaign_settings_file
        loaded: dict = quiet_parse(settings_file)
        loaded = merge_settings_dicts(new_data, loaded)
        with settings_file.open('w', newline="\n") as f:
            yaml.dump(loaded, f)

    def get_latest_planning_index(self, key: str) -> int:
        """Find the highest index in planning filenames

        Searches the filenames for either session or plot files to find the highest index within those names.
        Filenames must match campaign.x.filename_pattern, but the file type suffix is ignored. The string
        ((NNN)) is where this method will look for the index number (the total number of Ns is not relevant).

        If there are no matching files, the value from campaign.x.latest_index is returned instead.

        If there is no campaign_dir, a warning is logged and the value from campaign.x.latest_index is returned.

        Args:
            key (str): Type of planning file to examine. Must be one of "plot" or "session".

        Returns:
            int: Highest index number appearing within filenames that match the key's filename_pattern, or the
                 value of the key's latest_index setting.

        Raises:
            KeyError: When key is invalid.
        """
        if key not in ("plot", "session"):
            raise KeyError(f"Key must be one of 'plot' or 'session', got '{key}'")

        latest_number: int = self.get(f"campaign.{key}.latest_index")
        if not self.campaign_dir:
            logging.warning(f"No campaign dir when fetching latest {key} file")
            return latest_number

        planning_name = PlanningFilename(self.get(f"campaign.{key}.filename_pattern"))
        target_regex = re.compile(f"^{planning_name.index_capture_regex}$", flags=re.I)

        planning_dir: Path = self.campaign_dir / self.get(f"campaign.{key}.path")
        matches: list = [target_regex.match(f.stem) for f in planning_dir.glob("*.*")]
        plot_numbers: list[int] = [int(match.group('number')) for match in matches if match]

        if plot_numbers:
            latest_number = max(plot_numbers)
            self.patch_campaign_settings({key: {"latest_index": latest_number}})

        return latest_number

    @property
    def latest_plot_index(self) -> int:
        """Get the largest index number in plot filenames

        Calls get_latest_planning_index("plot")

        Returns:
            int: Highest index of the plot files
        """
        return self.get_latest_planning_index("plot")

    @property
    def latest_session_index(self) -> int:
        """Get the largest index number in session filenames

        Calls get_latest_planning_index("session")

        Returns:
            int: Highest index of the session files
        """
        return self.get_latest_planning_index("session")

    @property
    def plot_dir(self) -> Path:
        """Get the path to the current campaign's plot directory

        Returns:
            Path: Path to the campaign's plot directory, or None if campaign_dir is not set
        """
        if not self.campaign_dir:
            return None

        return self.campaign_dir / self.get("campaign.plot.path")

    @property
    def session_dir(self) -> Path:
        """Get the path to the current campaign's sessions directory

        Returns:
            Path: Path to the campaign's sessions directory, or None if campaign_dir is not set
        """
        if not self.campaign_dir:
            return None

        return self.campaign_dir / self.get("campaign.session.path")

    @property
    def characters_dir(self) -> Path:
        """Get the path to the current campaign's characters directory

        Returns:
            Path: Path to the campaign's characters directory, or None if campaign_dir is not set
        """
        if not self.campaign_dir:
            return None

        return self.campaign_dir / self.get("campaign.characters.path")
