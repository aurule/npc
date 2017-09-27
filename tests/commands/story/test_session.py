import npc

def test_makes_files(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.session()
    assert result.success
    assert campaign.get_file('Session History', 'session 2.md').check()
    assert campaign.get_file('Plot', 'plot 2.md').check()

def test_imbalanced_files(campaign):
    campaign.populate_from_fixture_dir('session', 'imbalanced')
    result = npc.commands.story.session()
    assert result.success # works
    assert campaign.get_file('Plot', 'plot 2.md').check() #creates the file

def test_no_files(campaign):
    """When the directories exist, but there are no plot or session files, the
    command should create some base files."""

    campaign.populate_from_fixture_dir('session', 'empty')
    result = npc.commands.story.session()
    assert result.success
    assert campaign.get_file('Session History', 'session 1.md').check()
    assert campaign.get_file('Plot', 'plot 1.md').check()
