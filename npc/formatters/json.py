import json
from .. import commands

def dump(characters, f, meta):
    if meta:
        json.dump([meta] + characters, f)
    else:
        json.dump(characters, f)

    return commands.Result(True)
