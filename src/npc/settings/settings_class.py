"""
Load and save settings info
"""

import yaml
from collections import defaultdict
from importlib import resources
from functools import cached_property
from packaging.version import Version
from os import getenv

from pathlib import Path
from npc import __version__ as npc_version
from npc.util import DataStore, ParseError
from npc.util.functions import merge_data_dicts, prepend_namespace
from .tags import make_deprecated_tag_specs
from .helpers import quiet_parse
from .systems import System

import logging
logger = logging.getLogger(__name__)

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
        self.versions = {
            "package": npc_version,
        }
        self.loaded_paths = {
            "package": None,
        }

        # load defaults and user prefs
        self.refresh()

    def refresh(self) -> None:
        """
        Clear internal data, and refresh the default and personal settings files
        """
        self.data = {}
        self.load_settings_file(self.default_settings_path / "settings.yaml", file_key="internal")
        self.load_systems(self.default_settings_path / "systems")
        self.load_settings_file(self.personal_dir / "settings.yaml", file_key="user")
        self.load_systems(self.personal_dir / "systems")

    def load_settings_file(self, settings_file: Path, namespace: str = None, *, file_key: str = None) -> None:
        """Open, parse, and merge settings from another file

        This is the primary way to load more settings info. Passing in a file path that does not exist will
        result in a log message and no error, since all setting files are technically optional.

        The file_key for any given file should be unique. These are the keys in use right now:
        * internal
        * user
        * campaign

        Args:
            settings_file (Path): The file to load
            namespace (str): Optional namespace to use for new_data
            file_key (str): Key to use when storing the file's stated npc version and path
        """
        loaded: dict = quiet_parse(settings_file)
        if loaded is None:
            fallbacks = [
                settings_file.parent / "settings.json",
                settings_file.parent / "settings.yml",
            ]
            if file_key and any([f.exists() for f in fallbacks]):
                file_version = "1.0.0"
                self.versions[file_key] = "1.0.0"
                self.loaded_paths[file_key] = settings_file.parent
            return

        if file_key:
            file_version = loaded.get("npc", {}).pop("version", None)
            self.versions[file_key] = file_version
            self.loaded_paths[file_key] = settings_file

        self.merge_data(loaded, namespace)

    def package_outdated(self, location: str):
        """Check if a loaded settings file is from a newer version of NPC

        NPC is intended to be strongly backwards compatable within major versions,
        with breaking changes to settings handled by the migration system. This means
        that it's usually ok to simply warn the user instead of interrupt the action
        they want to take.

        Args:
            location (str): Settings location to check. Typically one of "user" or "campaign".
        """

        # Skip outdated warning during unrelated testing. Other tests often run
        # with intentionally incomplete or incorrect settings.
        current_test = getenv("PYTEST_CURRENT_TEST", None)
        if current_test and not "test_package_outdated" in current_test:
            return False

        package_version = Version(npc_version)
        raw_settings_version = self.versions.get(location) or npc_version
        settings_version = Version(raw_settings_version)

        return package_version < settings_version

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

            system_name = next(iter(loaded))
            loaded_contents = loaded[system_name]

            if "extends" in loaded_contents:
                dependencies[loaded_contents["extends"]].append(loaded)
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
                    child_name = next(iter(child))
                    parent_conf = dict(self.get(f"npc.systems.{parent_name}"))
                    combined = merge_data_dicts(child[child_name], parent_conf)
                    self.merge_data(combined, namespace=f"npc.systems.{child_name}")
            if not new_deps:
                return
            if new_deps == deps:
                logger.error(f"Some systems could not be found: {deps.keys()}")
                return
            load_dependencies(new_deps)

        load_dependencies(dependencies)

    def load_types(self, types_dir: Path, *, system_key: str, namespace_root: str = "npc") -> None:
        """Load type definitions from a path for a given game system

        Parses and stores type definitions found in types_dir. All yaml files in that dir are assumed to be
        type defs. Files immediately in the dir are parsed first, then a subdir matching the given system key
        is checked.

        Parsed definitions are put into the "x.types.system" namespace. The root of this namespace is
        determined by the namespace_root passed, and the system component uses the system key provided.

        The sheet_path property is handled specially. If it's present in a type's yaml, then that value is
        used. If not, a file whose name matches the type key is assumed to be the correct sheet contents file.

        Args:
            types_dir (Path): Path to look in for type definitions
            system_key (str): Key of the game system these types are for
            namespace_root (str): [description] (default: `"npc"`)
        """
        def process_types_dir(search_dir: Path) -> None:
            """Load yaml files, expand sheet paths, handle implied sheets

            This internal helper method scans all the files in search_dir and tries to load them by their type:
            * yaml files are treated as type definitions and parsed. If they have a sheet_path property, it is
              expanded into a fully qualified Path for later use
            * All other files are set aside for later. After the types have been loaded, the base names of the
              remaining files are compared against the loaded type keys within our current namespace. Any that
              match are treated as the implicit sheet file for that type, and their Path is saved to the
              type's sheet_path property.

            Args:
                search_dir (Path): Directory to search for type and sheet files
            """
            discovered_sheets: dict = {}
            for type_path in search_dir.glob("*.*"):
                if type_path.suffix != ".yaml":
                    type_key: str = type_path.stem
                    discovered_sheets[type_key] = type_path
                    continue

                typedef: dict = quiet_parse(type_path)
                try:
                    type_key: str = next(iter(typedef))
                except TypeError:
                    raise ParseError("Missing top-level key for type config", type_path)

                if typedef[type_key].get("sheet_path"):
                    sheet_path = Path(typedef[type_key].get("sheet_path"))
                    if sheet_path.is_absolute():
                        typedef[type_key]["sheet_path"] = sheet_path.resolve()
                    else:
                        typedef[type_key]["sheet_path"] = search_dir.joinpath(sheet_path).resolve()

                self.merge_data(typedef, types_namespace)

            for type_key, sheet_path in discovered_sheets.items():
                if type_key not in self.get(types_namespace, {}):
                    logger.info(f"Type {type_key} not defined, skipping potential sheet {sheet_path}")
                    continue
                if "sheet_path" not in self.get(f"{types_namespace}.{type_key}"):
                    self.merge_data({type_key: {"sheet_path": sheet_path}}, types_namespace)

        types_namespace: str = f"{namespace_root}.types.{system_key}"
        process_types_dir(types_dir)
        if self.get(f"npc.systems.{system_key}.extends"):
            process_types_dir(types_dir / self.get(f"npc.systems.{system_key}.extends"))
        process_types_dir(types_dir / system_key)

    @property
    def systems(self) -> list[System]:
        """Get all configured systems

        Returns:
            list[System]: List of System objects
        """
        return [System(s, self) for s in self.get("npc.systems")]

    def get_system_keys(self) -> list[str]:
        """Get a list of valid system keys

        This method only considers systems in the npc namespace.

        Returns:
            list[str]: List of system keys
        """
        return self.get("npc.systems").keys()

    def get_system(self, key: str) -> System:
        """Get a system object for the given system key

        Creates a System object using the definition from the given key. If the key does not have a
        definition, returns None.

        Args:
            key (str): System key name to use

        Returns:
            System: System object for the given key, or None if the key does not have a system def
        """
        if key not in self.get("npc.systems"):
            logger.error(f"System '{key}' is not defined")
            return None

        return System(key, self)

    @cached_property
    def deprecated_tags(self) -> dict:
        """Get the deprecated tag definitions

        These specs describe tags that should no longer be used at all, due to changes in the way that NPC
        works.

        Returns:
            dict: Dict of deprecated tag info, indexed by tag name
        """
        return make_deprecated_tag_specs(self.get("npc.deprecated_tags", {}))

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
        campaign.create_on_init. All paths are to be interpreted as relative to the campaign's root.

        Returns:
            list: List of directory names to create on campaign init
        """
        return self.required_dirs + self.get("campaign.create_on_init")
