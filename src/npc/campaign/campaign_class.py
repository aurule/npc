from pathlib import Path

from ..settings import Settings, PlanningFilename

class Campaign:
    def __init__(self, campaign_path: Path, *, settings: Settings = None):
        self.root = campaign_path

        if settings is None:
            settings = Settings()
        self.settings = settings

        settings.load_campaign(campaign_path)

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
        if not self.settings.campaign_dir:
            logging.warning("No campaign dir in settings, cannot create planning files")
            return None

        latest_plot = self.settings.latest_plot_index
        latest_session = self.settings.latest_session_index

        max_existing_index = max(latest_plot, latest_session)
        incremented_index = min(latest_plot, latest_session) + 1
        new_index = max(max_existing_index, incremented_index)

        return_paths = {}
        for key in ["plot", "session"]:
            name_pattern = PlanningFilename(self.settings.get(f"campaign.{key}.filename_pattern"))
            new_filename = name_pattern.for_index(new_index)
            new_path = self.settings.campaign_dir / self.settings.get(f"campaign.{key}.path") / new_filename
            return_paths[key] = new_path
            if not new_path.exists():
                self.settings.patch_campaign_settings({key: {"latest_index": new_index}})
                new_path.write_text(self.settings.get(f"campaign.{key}.file_contents"), newline = "\n")

        return return_paths
