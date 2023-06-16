"""
Package for the npc command-line program
"""

try:
    import click, sqlalchemy
    from rich.traceback import install
    install(suppress=[click, sqlalchemy])
except ImportError:
    pass

from .commands.main_group import cli
