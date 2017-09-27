import npc

def test_find_plot(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('both')
    assert result.success
    assert result.openable == ['Plot/plot 1.md', 'Session History/session 1.md']

def test_find_session(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('session')
    assert result.success
    assert result.openable == ['Session History/session 1.md']

def test_find_latest(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('plot')
    assert result.success
    assert result.openable == ['Plot/plot 1.md']
