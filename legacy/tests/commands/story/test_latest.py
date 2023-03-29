import npc

def test_find_unrecognized(campaign):
    """When the argument is unrecognized"""

    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('asdf')
    assert result.success
    assert result.openable == ['Session History/Session 1.md', 'Plot/Plot 1.md']

def test_find_blank(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest()
    assert result.success
    assert result.openable == ['Session History/Session 1.md', 'Plot/Plot 1.md']

def test_find_session(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('session')
    assert result.success
    assert result.openable == ['Session History/Session 1.md']

def test_find_plot(campaign):
    campaign.populate_from_fixture_dir('session', 'balanced')
    result = npc.commands.story.latest('plot')
    assert result.success
    assert result.openable == ['Plot/Plot 1.md']
