"""
Package for reading and manipulating campaign information.
"""

from .cli import start as start_cli
from .gui import start as start_gui
from .util import find_campaign_root, Character

VERSION = "1.3.0 alpha 1"
"""str: Current code version"""
