"""
CLI command functions

These functions are a facade on top of the npc library. Designed to be run from the CLI.
"""

from npc import commands

def _serialize(*argnames, **full_args):
    serial_args = [full_args.pop(k) for k in argnames]
    return serial_args, full_args

def reorg(kwargs):
    serial_args, keyword_args = _serialize('search', **kwargs)
    return commands.reorg(*serial_args, **keyword_args)

def dump(kwargs):
    serial_args, keyword_args = _serialize('search', **kwargs)
    return commands.dump(*serial_args, **keyword_args)

def lint(kwargs):
    serial_args, keyword_args = _serialize('search', **kwargs)
    return commands.lint(*serial_args, **keyword_args)

def init(kwargs):
    return commands.init(**kwargs)

def open_settings(kwargs):
    serial_args, keyword_args = _serialize('location', **kwargs)
    return commands.open_settings(*serial_args, **keyword_args)

def report(kwargs):
    serial_args, keyword_args = _serialize('tags', **kwargs)
    return commands.report(*serial_args, **keyword_args)

def find(kwargs):
    serial_args, keyword_args = _serialize('rules', **kwargs)
    return commands.find(*serial_args, **keyword_args)

def create_standard(kwargs):
    serial_args, keyword_args = _serialize('name', 'ctype', **kwargs)
    return commands.create_character.standard(*serial_args, **keyword_args)

def create_changeling(kwargs):
    serial_args, keyword_args = _serialize('name', 'seeming', 'kith', **kwargs)
    return commands.create_character.changeling(*serial_args, **keyword_args)

def make_list(kwargs):
    serial_args, keyword_args = _serialize('search', **kwargs)
    return commands.listing.make_list(*serial_args, **keyword_args)

def session(kwargs):
    return commands.story.session(**kwargs)

def latest(kwargs):
    serial_args, keyword_args = _serialize('thingtype', **kwargs)
    return commands.story.latest(*serial_args, **keyword_args)
