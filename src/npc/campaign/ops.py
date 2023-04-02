"""Functions that perform campaign management operations

These functions create or manipulate general campaign files. They do not affect characters, despite those
being contained within a campaign.
"""
import yaml
from pathlib import Path

from . import helpers
from ..settings import Settings

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
