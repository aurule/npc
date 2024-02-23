from PySide6.QtGui import QIcon

from . import resources

import logging
logger = logging.getLogger(__name__)

def theme_or_resource_icon(name: str) -> QIcon:
    return QIcon.fromTheme(name, QIcon(f":/icons/{name}"))

def find_settings_file(settings, location: str) -> str:
    """Find or create the desired settings file, if possible

    Looks for either the user or campaign settings file.

    Both locations are pulled from settings.

    Args:
        settings (Settings): Settings file to use to find the settings files
        location (str): File location key. One of "user" or "campaign"

    Returns:
        str: String describing the settings file location
    """
    match location:
        case "user":
            target_file = settings.personal_dir / "settings.yaml"
        case "campaign":
            target_file = settings.campaign_dir / ".npc" / "settings.yaml"
        case _:
            logger.error(f"Unrecognized settings location '{location}'")
            return None

    if not target_file.exists():
        return None

    return str(target_file)
