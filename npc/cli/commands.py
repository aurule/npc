"""
CLI command functions

These functions are a facade on top of the npc library. Designed to be run from the CLI.
"""

from npc import commands

def reorg(*args, **kwargs):
    return commands.reorg(*args, **kwargs)

def dump(*args, **kwargs):
    return commands.dump(*args, **kwargs)

def lint(*args, **kwargs):
    return commands.lint(*args, **kwargs)

def init(**kwargs):
    return commands.init(**kwargs)

def open_settings(*args, **kwargs):
    return commands.open_settings(*args, **kwargs)

def report(*args, **kwargs):
    return commands.report(*args, **kwargs)

def find(*args, **kwargs):
    return commands.find(*args, **kwargs)

def create_standard(*args, **kwargs):
    return commands.create_character.standard(*args, **kwargs)

def create_changeling(*args, **kwargs):
    return commands.create_character.changeling(*args, **kwargs)

def make_list(*args, **kwargs):
    return commands.listing.make_list(*args, **kwargs)

def session(**kwargs):
    return commands.story.session(**kwargs)

def latest(*args, **kwargs):
    return commands.story.latest(*args, **kwargs)
