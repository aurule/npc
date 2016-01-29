import json
from .. import commands

def dump(characters, f, meta):
    if meta:
        characters = [meta] + characters

    json.dump(characters, f)
    return commands.Result(True)
