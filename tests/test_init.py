import npc
import os

def test_init_bare(argparser, prefs, campaign):
    args = argparser.parse_args(['init'])
    npc.commands.init(args, prefs)
    for k, p in prefs.get('paths').items():
        assert os.path.exists(p)

def test_init_types(argparser, prefs, campaign):
    args = argparser.parse_args(['init', '-t'])
    npc.commands.init(args, prefs)
    for k, path in prefs.get('type_paths').items():
        assert os.path.exists(os.path.join(prefs.get('paths.characters'), path))

def test_init_all(argparser, prefs, campaign):
    args = argparser.parse_args(['init', '-a'])
    npc.commands.init(args, prefs)
    for k, path in prefs.get('type_paths').items():
        assert os.path.exists(os.path.join(prefs.get('paths.characters'), path))
