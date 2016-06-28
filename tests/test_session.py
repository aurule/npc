import npc

def test_makes_files(campaign, argparser, prefs):
    campaign.populate_from_fixture_dir(['session', 'balanced'])
    args = argparser.parse_args(['session'])
    result = npc.commands.session(args, prefs)
    assert result.success
    assert campaign.get_file('Session History', 'session 2.md').check()
    assert campaign.get_file('Plot', 'plot 2.md').check()

def test_imbalanced_files(campaign, argparser, prefs):
    campaign.populate_from_fixture_dir(['session', 'imbalanced'])
    args = argparser.parse_args(['session'])
    result = npc.commands.session(args, prefs)
    assert result.success # works
    assert campaign.get_file('Plot', 'plot 2.md').check() #creates the file

def test_no_files(campaign, argparser, prefs):
    """When the directories exist, but there are no plot or session files, the
    command should create some base files."""

    campaign.populate_from_fixture_dir(['session', 'empty'])
    args = argparser.parse_args(['session'])
    result = npc.commands.session(args, prefs)
    assert result.success
    assert campaign.get_file('Session History', 'session 1.md').check()
    assert campaign.get_file('Plot', 'plot 1.md').check()
