"""
Package for the NPC Campaign Manager graphical program
"""

try:
    from rich.traceback import install
    import click, sqlalchemy, PySide6
    install(suppress=[click, sqlalchemy, PySide6])
except ImportError:
    pass

from .runner import run
