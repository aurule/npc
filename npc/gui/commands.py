"""
GUI command functions

These functions are a facade on top of the npc library. Designed to be run from the GUI.
"""

from npc import commands

def init(**kwargs):
    return commands.init(**kwargs)

def open_settings(*args, **kwargs):
    return commands.open_settings(*args, **kwargs)

def find_characters(*args):
    return commands.find_characters(*args)

def create_standard(kwargs):
    serial_args, keyword_args = _serialize('name', 'ctype', **kwargs)
    return commands.create_character.standard(*serial_args, **keyword_args)

def create_changeling(kwargs):
    serial_args, keyword_args = _serialize('name', 'seeming', 'kith', **kwargs)
    return commands.create_character.changeling(*serial_args, **keyword_args)

def session(**kwargs):
    return commands.story.session(**kwargs)

def latest(*args, **kwargs):
    return commands.story.latest(*args, **kwargs)
