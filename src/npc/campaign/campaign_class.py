import logging
import re
import yaml
from pathlib import Path

from ..settings import Settings, PlanningFilename
from ..util.functions import merge_data_dicts, prepend_namespace
from npc.settings.helpers import quiet_parse

class Campaign:
    def __init__(self, campaign_path: Path, *, settings: Settings = None):
        self.root = campaign_path

        if settings is None:
            settings = Settings()
        self.settings = settings

        self.settings.load_settings_file(self.settings_file)
        self.settings.load_systems(self.settings_dir / "systems")

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

    def patch_campaign_settings(self, data: dict) -> None:
        """Update some values in the campaign settings and corresponding file

        Updates the internal campaign settings with data, then writes those changes to the current campaign's
        settings file.

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
