"""
GUI command functions

These functions are a facade on top of the npc library. Designed to be run from the GUI.
"""

from npc import commands

def init(**kwargs):
    return commands.init(**kwargs)

def open_settings(*args, **kwargs):
    return commands.open_settings(*args, **kwargs)

def find_characters(*args, **kwargs):
    return commands.find_characters(*args, **kwargs)

def create_standard(*args, **kwargs):
    return commands.create_character.standard(*args, **kwargs)

def create_changeling(*args, **kwargs):
    return commands.create_character.changeling(*args, **kwargs)

def session(**kwargs):
    return commands.story.session(**kwargs)

def latest(*args, **kwargs):
    return commands.story.latest(*args, **kwargs)
