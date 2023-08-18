import re
import yaml
from pathlib import Path
from functools import cached_property, cache

from npc.settings import Settings, PlanningFilename, System
from npc.util.functions import merge_data_dicts, prepend_namespace
from npc.settings.helpers import quiet_parse
from npc.settings.types import make_types, TypeSpec, UndefinedTypeSpec
from npc.settings.tags import make_tags, make_metatag_specs, TagSpec, UndefinedTagSpec
from npc.settings.tag_definer_interface import TagDefiner
from .character_collection import CharacterCollection

@TagDefiner.register
class Campaign:
    def __init__(self, campaign_path: Path, *, settings: Settings = None):
        self.root = campaign_path

        if settings is None:
            settings = Settings()
        self.settings = settings

        self.settings.load_settings_file(self.settings_file, file_key="campaign")
        self.settings.load_systems(self.settings_dir / "systems")

        self.characters = CharacterCollection(self)

    @property
    def name(self) -> str:
        """Get the campaign's name

        Convenience property to pull the name from settings

        Returns:
            str: Name of the campaign
        """
        return self.settings.get("campaign.name")

    @property
    def desc(self) -> str:
        """Get the campaign's description

        Convenience property to pull the description from settings

        Returns:
            str: Description of the campaign
        """
        return self.settings.get("campaign.desc")

    @property
    def system_key(self) -> str:
        """Get the campaign's game system key

        Convenience property to pull the game system key from settings

        Returns:
            str: Description of the campaign
        """
        return self.settings.get("campaign.system")

    @property
    def system(self) -> System:
        """Get a System object for the campaign's game system

        Returns:
            System: System object with data about this campaign's game system
        """
        return System(self.system_key, self.settings)

    @property
    def plot_dir(self) -> Path:
        """Get the path to the current campaign's plot directory

        Returns:
            Path: Path to the campaign's plot directory, or None if campaign_dir is not set
        """

        return self.root / self.settings.get("campaign.plot.path")

    @property
    def session_dir(self) -> Path:
        """Get the path to the current campaign's sessions directory

        Returns:
            Path: Path to the campaign's sessions directory, or None if campaign_dir is not set
        """
        return self.root / self.settings.get("campaign.session.path")

    @property
    def characters_dir(self) -> Path:
        """Get the path to the current campaign's characters directory

        Returns:
            Path: Path to the campaign's characters directory, or None if campaign_dir is not set
        """
        return self.root / self.settings.get("campaign.characters.path")

    @property
    def settings_dir(self) -> Path:
        """Get the path to the current campaign settings directory

        Returns:
            Path: Path to the campaign's settings dir, or None if campaign_dir is not set
        """
        return self.root / ".npc"

    @property
    def settings_file(self) -> Path:
        """Get the path to the current campaign settings file

        Returns:
            Path: Path to the campaign's settings file, or None if campaign_dir is not set
        """
        return self.settings_dir / "settings.yaml"

    @cached_property
    def types(self) -> dict:
        """Get the character types for this campaign

        Loads the default, user, and campaign-specific types for the campaign's system and generates a dict
        of TypeSpec objects.

        Returns:
            dict: TypeSpec objects
        """
        self.system.load_types()
        self.settings.load_types(
            self.settings_dir / "types",
            system_key=self.system_key,
            namespace_root="campaign")
        type_defs = merge_data_dicts(
            self.settings.get(f"campaign.types.{self.system_key}", {}),
            self.settings.get(f"npc.types.{self.system_key}", {}))
        return make_types(type_defs)


    def get_type(self, type_key: str) -> TypeSpec:
        """Get a single character type

        Args:
            type_key (str): Key for the character type to get

        Returns:
            TypeSpec: TypeSpec for the given key, or an UndefinedType if that key does not have a type
        """
        return self.types.get(type_key, UndefinedTypeSpec(type_key))

    @property
    def campaign_tag_defs(self) -> dict:
        """Get the combined tag definitions for this campaign

        Merges the campaign-specific tags into the system tags and returns the resulting dict

        Returns:
            dict: Dict of tag configurations
        """

        system_tag_defs: dict = self.system.system_tag_defs
        campaign_tag_defs: dict = self.settings.get("campaign.tags", {})
        return merge_data_dicts(campaign_tag_defs, system_tag_defs)

    @cached_property
    def tags(self) -> dict:
        """Get the tags configured for this campaign

        Combines tag definitions from the system and this campaign

        Returns:
            dict: Dict of TagSpec objects indexed by tag key
        """
        return make_tags(self.campaign_tag_defs)

    def get_tag(self, tag_name: str) -> TagSpec:
        """Get a single tag as configured for this campaign

        Uses the combied system and campaign definitions

        Args:
            tag_name (str): Name of the tag to get

        Returns:
            TagSpec: Spec of the named tag, or a new UndefinedTagSpec if that tag has no definition
        """
        return self.tags.get(tag_name, UndefinedTagSpec(tag_name))

    @property
    def campaign_metatag_defs(self) -> dict:
        """Get the combined metatag definitions for this campaign

        Merges the campaign-specific metatags into the system metatags and returns the resulting dict

        Returns:
            dict: Dict of metatag configurations
        """

        system_metatag_defs: dict = self.system.system_metatag_defs
        campaign_metatag_defs: dict = self.settings.get("campaign.metatags", {})
        return merge_data_dicts(campaign_metatag_defs, system_metatag_defs)

    @cached_property
    def metatags(self) -> dict:
        """Get the metatags configured for this campaign

        Combines metatag definitions from the system and this campaign

        Returns:
            dict: Dict of MetatagSpec objects indexed by metatag key
        """
        return make_metatag_specs(self.campaign_metatag_defs)

    @cache
    def type_tags(self, type_key: str) -> dict:
        """Get the tags for a specific character type

        Combines core and system tags with any tags defined in the type itself

        Args:
            type_key (str): Key for the character type to get tags for

        Returns:
            dict: Dict of TagSpec objects indexed by tag key
        """
        char_type = self.get_type(type_key)

        type_tag_defs: dict = char_type.definition.get("tags", {})
        combined_defs = merge_data_dicts(type_tag_defs, self.campaign_tag_defs)
        return make_tags(combined_defs)

    def get_type_tag(self, tag_name: str, type_key: str) -> TagSpec:
        """Get a single tag as configured for this campaign and type

        Uses the combied system, campaign, and type definitions

        Args:
            tag_name (str): Name of the tag to get
            type_key (str): Key for the character type to get a tag for

        Returns:
            TagSpec: Spec of the named tag, or a new UndefinedTagSpec if that tag has no definition
        """
        return self.type_tags(type_key).get(tag_name, UndefinedTagSpec(tag_name))

    def bump_planning_files(self) -> dict:
        """Create the next planning files by current index

        Using the existing files (or saved indexes), this creates plot and session files for the next index. The
        logic is:
        1. If plot and session indexes are equal, increment both indexes and create a new file for each
        2. If one is greater than the other, update the lesser to equal the greater and create a file for the
           lesser. The greater file is left alone.

        Returns:
            dict: Dict containing the resulting file paths, whether new or old. They are indexed by type, so
                  "path" and "session" both will have an entry.
        """
        latest_plot = self.latest_plot_index
        latest_session = self.latest_session_index

        max_existing_index = max(latest_plot, latest_session)
        incremented_index = min(latest_plot, latest_session) + 1
        new_index = max(max_existing_index, incremented_index)

        return_paths = {}
        for key in ["plot", "session"]:
            name_pattern = PlanningFilename(self.settings.get(f"campaign.{key}.filename_pattern"))
            new_filename = name_pattern.for_index(new_index)
            new_path = self.root / self.settings.get(f"campaign.{key}.path") / new_filename
            return_paths[key] = new_path
            if not new_path.exists():
                self.patch_campaign_settings({key: {"latest_index": new_index}})
                new_path.write_text(self.settings.get(f"campaign.{key}.file_contents"), newline = "\n")

        return return_paths

    def get_latest_planning_index(self, key: str) -> int:
        """Find the highest index in planning filenames

        Searches the filenames for either session or plot files to find the highest index within those names.
        Filenames must match campaign.x.filename_pattern, but the file type suffix is ignored. The string
        ((NNN)) is where this method will look for the index number (the total number of Ns is not relevant).

        If there are no matching files, the value from campaign.x.latest_index is returned instead.

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

        latest_number: int = self.settings.get(f"campaign.{key}.latest_index")

        planning_name = PlanningFilename(self.settings.get(f"campaign.{key}.filename_pattern"))
        target_regex = re.compile(f"^{planning_name.index_capture_regex}$", flags=re.I)

        planning_dir: Path = self.root / self.settings.get(f"campaign.{key}.path")
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

    def get_latest_planning_file(self, key: str) -> Path:
        """Get the path to the highest-numbered planning file

        Searches the filenames for either session or plot files and returns the one with the highest index.

        Args:
            key (str): Type of planning file to get. Must be one of "plot" or "session".

        Returns:
            Path: Path to the highest-numbered planning file

        Raises:
            KeyError: When key is invalid.
        """
        if key not in ("plot", "session"):
            raise KeyError(f"Key must be one of 'plot' or 'session', got '{key}'")

        planning_dir: Path = self.root / self.settings.get(f"campaign.{key}.path")
        planning_name = PlanningFilename(self.settings.get(f"campaign.{key}.filename_pattern"))
        file_path = planning_dir / planning_name.for_index(self.get_latest_planning_index(key))

        if file_path.exists():
            return file_path

        return None

    def patch_campaign_settings(self, data: dict) -> None:
        """Update some values in the campaign settings and corresponding file

        Updates the internal campaign settings with data, then writes those changes to the current campaign's
        settings file. The data is wrapped in the campaign namespace automatically.

        If campaign_dir is not set, this returns immediately.

        Args:
            data (dict): Data to change
        """
        new_data = prepend_namespace(data, "campaign")
        self.settings.merge_data(new_data)

        settings_file = self.settings_file
        loaded: dict = quiet_parse(settings_file)
        loaded = merge_data_dicts(new_data, loaded)
        with settings_file.open('w', newline="\n") as f:
            yaml.dump(loaded, f)
