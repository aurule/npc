"""
CLI command functions

These functions are a facade on top of the npc library. Designed to be run from the CLI.
"""

from npc import commands, util

def reorg(kwargs):
    serial_args, keyword_args = util.serialize_args('search', **kwargs)
    return commands.reorg(*serial_args, **keyword_args)

def dump(kwargs):
    serial_args, keyword_args = util.serialize_args('search', **kwargs)
    kwargs['sort_by'] = list(map(lambda s: s.strip(), kwargs['sort_by'].split(',')))
    return commands.dump(*serial_args, **keyword_args)

def lint(kwargs):
    serial_args, keyword_args = util.serialize_args('search', **kwargs)
    return commands.lint(*serial_args, **keyword_args)

def init(kwargs):
    return commands.init(**kwargs)

def open_settings(kwargs):
    serial_args, keyword_args = util.serialize_args('location', **kwargs)
    return commands.open_settings(*serial_args, **keyword_args)

def report(kwargs):
    serial_args, keyword_args = util.serialize_args('tags', **kwargs)
    return commands.report(*serial_args, **keyword_args)

def find(kwargs):
    serial_args, keyword_args = util.serialize_args('rules', **kwargs)
    return commands.find(*serial_args, **keyword_args)

def create_standard(kwargs):
    serial_args, keyword_args = util.serialize_args('name', 'ctype', **kwargs)
    return commands.create_character.standard(*serial_args, **keyword_args)

def create_changeling(kwargs):
    serial_args, keyword_args = util.serialize_args('name', 'seeming', 'kith', **kwargs)
    return commands.create_character.changeling(*serial_args, **keyword_args)

def make_list(kwargs):
    serial_args, keyword_args = util.serialize_args('search', **kwargs)
    keyword_args = util.listify_args('sort_by', 'group_by')
    return commands.listing.make_list(*serial_args, **keyword_args)

def session(kwargs):
    return commands.story.session(**kwargs)

def latest(kwargs):
    serial_args, keyword_args = util.serialize_args('thingtype', **kwargs)
    return commands.story.latest(*serial_args, **keyword_args)
