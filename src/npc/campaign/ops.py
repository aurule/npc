"""Functions that perform campaign management operations

These functions create or manipulate general campaign files. They do not affect characters, despite those
being contained within a campaign.
"""
import yaml
import logging
from pathlib import Path

from ..settings import Settings, PlanningFilename

def init(campaign_path: str, *, name: str, system: str, desc: str = None, settings: Settings = None) -> Settings:
    """Initialize a directory with the basics for npc

    Creates a few folders and a basic campaign config file. Folders for characters, sessions, and paths are
    always created, along with the special .npc folder. Additional folders in the setting
    campaign.create_on_init will also be created.

    Created by default:
    campaign_root/
        .npc/
            settings.yaml
        Characters/         # From campaign.characters.path
        Plot/               # From campaign.plot.path
        Session History/    # From campaign.session.path

    Args:
        campaign_path (str): Location of the campaign directory to use
        name (str): Name of the campaign, saved to campaign settings
        system (str): Name of the system, saved to campaign settings
        desc (str): Description of the campaign, saved to campaign settings if supplied (default: `None`)
        settings (Settings): Existing settings object to use. If none is supplied, a new one will be created (default: `None`)

    Returns:
        Settings: Settings object with the new campaign loaded
    """
    config_contents: dict = {"campaign": {"name": name, "system": system}}
    if desc is not None:
        config_contents["campaign"]["desc"] = desc

    if settings is None:
        settings = Settings()

    campaign_dir = Path(campaign_path)
    config_dir = campaign_dir / ".npc"

    config_dir.mkdir(exist_ok = True)
    config_file = config_dir / "settings.yaml"
    with config_file.open('w', newline="\n") as f:
        yaml.dump(config_contents, f)

    for dirname in settings.init_dirs:
        target = campaign_dir / dirname
        target.mkdir(exist_ok = True)

    settings.load_campaign(campaign_dir)
    return settings

def find_campaign_root(starting_dir: str) -> Path:
    """Find the root dir of a campaign

    Walks backward up the current dir's parents until either
    a) The directory contains .npc/, at which point it returns that directory
    b) The directory is the filesystem root, at which point it returns None

    Args:
        starting_dir (Path|str): Path whose parents will be searched.

    Returns:
        Path: Directory to the campaign's root dir, or None if no config dir was found.
    """
    current_dir = Path(starting_dir)
    old_dir = Path('')
    while not current_dir.joinpath('.npc').is_dir():
        old_dir = current_dir
        current_dir = current_dir.parent
        if old_dir.samefile(current_dir):
            return None

    return current_dir

def bump_planning_files(settings: Settings) -> dict:
    """Create the next planning files by current index

    Using the existing files (or saved indexes), this creates plot and session files for the next index. The
    logic is:
    1. If plot and session indexes are equal, increment both indexes and create a new file for each
    2. If one is greater than the other, update the lesser to equal the greater and create a file for the
       lesser. The greater file is left alone.

    Args:
        settings (Settings): Settings object to use for paths, filename patterns, and new file contents

    Returns:
        dict: Dict containing the resulting file paths, whether new or old. They are indexed by type, so
              "path" and "session" both will have an entry.
    """
    if not settings.campaign_dir:
        logging.warning("No campaign dir in settings, cannot create planning files")
        return (None, None)

    latest_plot = settings.latest_plot_index
    latest_session = settings.latest_session_index

    max_existing_index = max(latest_plot, latest_session)
    incremented_index = min(latest_plot, latest_session) + 1
    new_index = max(max_existing_index, incremented_index)

    return_paths = {}
    for key in ["plot", "session"]:
        name_pattern = PlanningFilename(settings.get(f"campaign.{key}.filename_pattern"))
        new_filename = name_pattern.for_index(new_index)
        new_path = settings.campaign_dir / settings.get(f"campaign.{key}.path") / new_filename
        return_paths[key] = new_path
        if not new_path.exists():
            settings.patch_campaign_settings({key: {"latest_index": new_index}})
            new_path.write_text(settings.get(f"campaign.{key}.file_contents"), newline = "\n")

    return return_paths
