"""
Package for the npc command-line program
"""

try:
    from rich.traceback import install
    import click, sqlalchemy
    install(suppress=[click, sqlalchemy])
except ImportError:
    pass

from .commands.main_group import cli
