import npc
import os
import json

def test_init_bare(prefs, campaign):
    npc.commands.init(prefs=prefs)
    for k, p in prefs.get('paths.required').items():
        if k in ["additional_paths"]:
            continue
        assert os.path.exists(p)

def test_init_types(prefs, campaign):
    npc.commands.init(create_types=True, prefs=prefs)
    for path in prefs.get_type_paths():
        assert os.path.exists(os.path.join(prefs.get('paths.required.characters'), path))

def test_init_all(prefs, campaign):
    npc.commands.init(create_all=True, prefs=prefs)
    for path in prefs.get_type_paths():
        assert os.path.exists(os.path.join(prefs.get('paths.required.characters'), path))

def test_init_with_name(prefs, campaign):
    npc.commands.init(campaign_name='Super Game', prefs=prefs)
    assert os.path.exists(prefs.get_settings_path('campaign'))
    with open(prefs.get_settings_path('campaign'), 'r') as settings:
        parsed = json.load(settings)
        assert parsed['campaign'] == 'Super Game'

def test_init_dryrun(prefs, campaign):
    npc.commands.init(dryrun=True, prefs=prefs)
    for path in prefs.get_type_paths():
        assert not os.path.exists(os.path.join(prefs.get('paths.required.characters'), path))
