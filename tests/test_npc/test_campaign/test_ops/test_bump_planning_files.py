import pytest
from tests.fixtures import tmp_campaign
from npc.settings import Settings

from npc.campaign import bump_planning_files

def populate(settings: Settings, plots: int = 0, sessions: int = 0) -> None:
    for index in range(plots):
        settings.plot_dir.joinpath(f"Plot {index}.md").touch()
    for index in range(sessions):
        settings.session_dir.joinpath(f"Session {index}.md").touch()

class TestWithoutCampaignDir:
    def test_returns_nones(self):
        settings = Settings()

        result = bump_planning_files(settings)

        assert result == (None, None)

class TestWithLesserSession:
    def test_creates_new_session_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 4, sessions = 3)

        bump_planning_files(settings)

        assert settings.session_dir.joinpath("Session 03.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 4, sessions = 3)

        bump_planning_files(settings)

        assert settings.latest_session_index == 3

    def test_ignores_old_plot_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)
        latest_plot = settings.plot_dir.joinpath("Plot 03.md")
        latest_plot.write_text("test plot", newline="\n")

        bump_planning_files(settings)

        contents = latest_plot.read_text()
        assert contents == "test plot"

    def test_ignores_old_plot_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 4, sessions = 3)

        bump_planning_files(settings)

        assert settings.latest_plot_index == 3

    def test_returns_old_and_new_files(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)
        latest_plot = settings.plot_dir.joinpath("Plot 03.md")
        latest_plot.touch()

        result = bump_planning_files(settings)

        expected_session = settings.session_dir.joinpath("Session 03.md")
        assert result["plot"] == latest_plot
        assert result["session"] == expected_session

    def test_jumps_big_gap(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 5, sessions = 1)

        bump_planning_files(settings)

        assert settings.latest_session_index == 4

class TestWithLesserPlot:
    def test_creates_new_plot_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 4)

        bump_planning_files(settings)

        assert settings.plot_dir.joinpath("Plot 03.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 4)

        bump_planning_files(settings)

        assert settings.latest_plot_index == 3

    def test_ignores_old_session_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)
        latest_session = settings.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        bump_planning_files(settings)

        contents = latest_session.read_text()
        assert contents == "test session"

    def test_ignores_old_session_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)
        latest_session = settings.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        bump_planning_files(settings)

        assert settings.latest_session_index == 3

    def test_returns_old_and_new_files(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)
        latest_session = settings.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        result = bump_planning_files(settings)

        expected_plot = settings.plot_dir.joinpath("Plot 03.md")
        assert result["session"] == latest_session
        assert result["plot"] == expected_plot

    def test_jumps_big_gap(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 1, sessions = 5)

        bump_planning_files(settings)

        assert settings.latest_plot_index == 4

class TestWithMatchingIndexes:
    def test_creates_new_plot_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)

        bump_planning_files(settings)

        assert settings.plot_dir.joinpath("Plot 03.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)

        bump_planning_files(settings)

        assert settings.latest_plot_index == 3

    def test_creates_new_session_file(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)

        bump_planning_files(settings)

        assert settings.session_dir.joinpath("Session 03.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)

        bump_planning_files(settings)

        assert settings.latest_session_index == 3

    def test_returns_both_files(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        populate(settings, plots = 3, sessions = 3)

        result = bump_planning_files(settings)

        expected_plot = settings.plot_dir.joinpath("Plot 03.md")
        expected_session = settings.session_dir.joinpath("Session 03.md")
        assert result["plot"] == expected_plot
        assert result["session"] == expected_session
