import pytest
from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def populate(campaign: Campaign, plots: int = 0, sessions: int = 0) -> None:
    for index in range(plots):
        campaign.plot_dir.joinpath(f"Plot {index}.md").touch()
    for index in range(sessions):
        campaign.session_dir.joinpath(f"Session {index}.md").touch()

class TestWithLesserSession:
    def test_creates_new_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.session_dir.joinpath("Session 03.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 3

    def test_ignores_old_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        latest_plot.write_text("test plot", newline="\n")

        tmp_campaign.bump_planning_files()

        contents = latest_plot.read_text()
        assert contents == "test plot"

    def test_ignores_old_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 3

    def test_returns_old_and_new_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        latest_plot.touch()

        result = tmp_campaign.bump_planning_files()

        expected_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        assert result["plot"] == latest_plot
        assert result["session"] == expected_session

    def test_jumps_big_gap(self, tmp_campaign):
        populate(tmp_campaign, plots = 5, sessions = 1)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 4

class TestWithLesserPlot:
    def test_creates_new_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.plot_dir.joinpath("Plot 03.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 3

    def test_ignores_old_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        tmp_campaign.bump_planning_files()

        contents = latest_session.read_text()
        assert contents == "test session"

    def test_ignores_old_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 3

    def test_returns_old_and_new_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        result = tmp_campaign.bump_planning_files()

        expected_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        assert result["session"] == latest_session
        assert result["plot"] == expected_plot

    def test_jumps_big_gap(self, tmp_campaign):
        populate(tmp_campaign, plots = 1, sessions = 5)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 4

class TestWithMatchingIndexes:
    def test_creates_new_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.plot_dir.joinpath("Plot 03.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 3

    def test_creates_new_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.session_dir.joinpath("Session 03.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 3

    def test_returns_both_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        result = tmp_campaign.bump_planning_files()

        expected_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        expected_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        assert result["plot"] == expected_plot
        assert result["session"] == expected_session
