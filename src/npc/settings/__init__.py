from .settings_class import Settings
from .planning_filename import PlanningFilename
from .systems import System
from .tags import Tag, DeprecatedTag

from pathlib import Path
from click import get_app_dir

def app_settings(app_name: str = "NPC") -> Settings:
    r"""Get a settings object with a platform-specific personal settings dir

    Different systems expect different locations for an app's user settings. This function creates a Settings
    object that loads and stores user settings to the appropriate directory based on the host system.

    OSX: ~/Library/Application Support/NPC
    Unix: ~/.config/npc
    Windows: C:\Users\<user>\AppData\Roaming\NPC

    Args:
        app_name (str): The application name. Defaults to NPC. Using a different name will give that
            application unexpected user settings. (default: `"NPC"`)

    Returns:
        Settings: Settings object with a platform-dependent user dir
    """
    return Settings(personal_dir = Path(get_app_dir(app_name)))
