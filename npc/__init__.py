"""
Package for reading and manipulating campaign information.
"""

from .cli import start as start_cli
from .gui import start as start_gui
from .util import find_campaign_root
from .util import Character

VERSION = "1.0.0"
"""str: Current code version"""
