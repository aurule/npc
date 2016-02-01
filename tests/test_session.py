import npc

# tests:
# fails on imbalanced numbers
# fails on missing files

def test_makes_files(campaign, argparser, prefs):
    campaign.populate_from_fixture_dir(['session', 'balanced'])
    args = argparser.parse_args(['session'])
    result = npc.commands.session(args, prefs)
    assert result.success
    assert campaign.get_file('Session History', 'session 2.md').check()
    assert campaign.get_file('Plot', 'Plot 2.md').check()

def test_imbalanced_files(campaign, argparser, prefs):
    campaign.populate_from_fixture_dir(['session', 'imbalanced'])
    args = argparser.parse_args(['session'])
    result = npc.commands.session(args, prefs)
    assert not result.success
    assert not campaign.get_file('Plot', 'plot 2.md').check()
