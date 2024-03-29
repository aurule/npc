"""
Helper functions unique to the settings module
"""

from pathlib import Path

from npc.util.errors import ParseError
from npc.util.functions import parse_yaml

import logging
logger = logging.getLogger(__name__)

def quiet_parse(settings_file: Path) -> dict:
    """Parse a yaml file and send log messages for common errors
    
    Parses a yaml file while suppressing exceptions for missing files or parse problems
    
    Args:
        settings_file (Path): Path to the yaml file to load
    
    Returns:
        dict: Parsed contents of the yaml file
    """
    try:
        loaded: dict = parse_yaml(settings_file)
    except OSError as err:
        # Settings are optional, so we silently ignore these errors
        logger.info('Missing settings file %s', settings_file)
        return None
    except ParseError as err:
        logger.warning(err.strerror)
        return None

    return loaded
