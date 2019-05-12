import npc

def test_requires_plot_path(campaign):
    """When the directories do not exist"""

    campaign.mkdir('Session History')
    result = npc.commands.story.session()
    assert not result.success

def test_requires_session_history_path(campaign):
    """When the directories do not exist"""

    campaign.mkdir('Plot')
    result = npc.commands.story.session()
    assert not result.success

class TestBalancedFiles:
    """Old plot and session both exist, with matching numbers"""

    def test_uses_next_number(self, campaign):
        campaign.populate_from_fixture_dir('session', 'balanced')
        result = npc.commands.story.session()
        assert result.success
        assert campaign.get_file('Session History', 'Session 2.md').exists()
        assert campaign.get_file('Plot', 'Plot 2.md').exists()

    def test_opens_all_files(self, campaign):
        campaign.populate_from_fixture_dir('session', 'balanced')
        result = npc.commands.story.session()
        assert result.success
        assert 'Session History/Session 1.md' in result.openable
        assert 'Session History/Session 2.md' in result.openable
        assert 'Plot/Plot 1.md' in result.openable
        assert 'Plot/Plot 2.md' in result.openable

    def test_creates_extras(self, campaign, prefs):
        campaign.populate_from_fixture_dir('session', 'balanced')
        prefs.load_more(campaign.get_file('.npc', 'settings.json'))
        result = npc.commands.story.session(prefs=prefs)
        assert result.success
        assert campaign.get_file('Session History', 'Session 2 - XP.md').exists()
        assert campaign.get_file('Plot', 'Plot 2 - relationships.md').exists()

class TestOutdatedPlot:
    """Old plot and session exist, but plot is one behind session"""

    def test_creates_missing_plot(self, campaign):
        campaign.populate_from_fixture_dir('session', 'outdated-plot')
        result = npc.commands.story.session()
        assert result.success # works
        assert campaign.get_file('Plot', 'Plot 2.md').exists() #creates the file

class TestOutdatedSession:
    """Old plot and session exist, but session is one behind plot"""

    def test_creates_missing_session(self, campaign):
        campaign.populate_from_fixture_dir('session', 'outdated-session')
        result = npc.commands.story.session()
        assert result.success # works
        assert campaign.get_file('Session History', 'Session 2.md').exists() #creates the file

class TestEmptyFolders:
    """No plot or session files exist"""

    def test_creates_initial_files(self, campaign):
        campaign.populate_from_fixture_dir('session', 'empty')
        result = npc.commands.story.session()
        assert result.success
        assert campaign.get_file('Session History', 'Session 1.md').exists()
        assert campaign.get_file('Plot', 'Plot 1.md').exists()

    def test_opens_new_files(self, campaign):
        campaign.populate_from_fixture_dir('session', 'empty')
        result = npc.commands.story.session()
        assert result.success
        assert 'Session History/Session 1.md' in result.openable
        assert 'Plot/Plot 1.md' in result.openable

class TestSubstitution:
    """NNN and ((COPY)) should behave correctly"""

    def test_new_number(self, campaign, prefs):
        campaign.populate_from_fixture_dir('session', 'substitution')
        prefs.load_more(campaign.get_file('.npc', 'settings.json'))
        result = npc.commands.story.session(prefs=prefs)
        assert result.success

        session_file = campaign.get_file('Session History', 'Session 2.md')
        assert '2' in session_file.read_text()

    def test_copies_contents(self, campaign):
        campaign.populate_from_fixture_dir('session', 'substitution')
        result = npc.commands.story.session()
        assert result.success

        plot_file = campaign.get_file('Plot', 'Plot 2.md')
        assert 'asdf' in plot_file.read_text()

    def test_copies_blank(self, campaign):
        """There's nothing to copy, so insert a blank string instead"""

        campaign.populate_from_fixture_dir('session', 'empty')
        result = npc.commands.story.session()
        assert result.success

        plot_file = campaign.get_file('Plot', 'Plot 1.md')
        assert plot_file.read_text() == "\n"
