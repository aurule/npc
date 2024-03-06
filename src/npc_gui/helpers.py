from PySide6.QtGui import QIcon

from npc.settings import Settings

from . import resources

import logging
logger = logging.getLogger(__name__)

def fetch_icon(name: str) -> QIcon:
    """Get a theme icon or fall back on a local svg

    This gets a named icon from the system theme, or falls back on an icon
    resource if the theme has no icon. This is mostly useful on linux systems
    where KDE supplies icons.

    This means that our icon resources need to have the same names as standard
    KDE icons. When adding a new icon name, first see if one from
    [freedesktop.org](https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html)
    fits, then use the Cuttlefish KDE app to see if KDE has a suitable icon. If
    either of those works, use that icon's name. Otherwise, pick an icon name
    that makes sense. No matter what, add a new fallback icon from
    [Flowbite](https://flowbite.com/icons/). The fallback will be used on all
    Windows and Mac systems, as well as any Linux systems which do not have a
    KDE theme installed.

    Args:
        name (str): Name of the icon

    Returns:
        QIcon: Icon resource
    """
    return QIcon.fromTheme(name, QIcon(f":/icons/{name}"))

def find_settings_file(settings: Settings, location: str) -> str:
    """Locate the desired settings file

    Looks for either the user or campaign settings file. Both locations are
    pulled from settings.

    Args:
        settings (Settings): Settings file to use to find the settings files
        location (str): File location key. One of "user" or "campaign"

    Returns:
        str: String describing the settings file location, or None if the file does not exist
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
