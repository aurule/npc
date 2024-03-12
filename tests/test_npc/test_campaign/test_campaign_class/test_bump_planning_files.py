import pytest
from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def populate(campaign: Campaign, plots: int = 0, sessions: int = 0) -> None:
    if plots:
        for index in range(1, plots+1):
            campaign.plot_dir.joinpath(f"Plot {index:0>2}.md").touch()
    if sessions:
        for index in range(1, sessions+1):
            campaign.session_dir.joinpath(f"Session {index:0>2}.md").touch()

def test_copies_plot_contents(tmp_campaign):
    populate(tmp_campaign, plots = 1, sessions = 1)
    tmp_campaign.plot_dir.joinpath("Plot 01.md").write_text("test plot")

    result = tmp_campaign.bump_planning_files()

    assert result["plot"].read_text() == "test plot"

class TestWithLesserSession:
    def test_creates_new_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.session_dir.joinpath("Session 04.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 4

    def test_ignores_old_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 2)
        latest_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        latest_plot.write_text("test plot", newline="\n")

        tmp_campaign.bump_planning_files()

        contents = latest_plot.read_text()
        assert contents == "test plot"

    def test_ignores_old_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 4, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 4

    def test_returns_old_and_new_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 2)
        latest_plot = tmp_campaign.plot_dir.joinpath("Plot 03.md")
        latest_plot.touch()

        result = tmp_campaign.bump_planning_files()

        expected_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        assert result["plot"] == latest_plot
        assert result["session"] == expected_session

    def test_jumps_big_gap(self, tmp_campaign):
        populate(tmp_campaign, plots = 5, sessions = 1)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 5

class TestWithLesserPlot:
    def test_creates_new_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.plot_dir.joinpath("Plot 04.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 4

    def test_ignores_old_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)
        latest_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        tmp_campaign.bump_planning_files()

        contents = latest_session.read_text()
        assert contents == "test session"

    def test_ignores_old_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)
        latest_session = tmp_campaign.session_dir.joinpath("Session 03.md")
        latest_session.write_text("test session", newline="\n")

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 4

    def test_returns_old_and_new_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 4)
        latest_session = tmp_campaign.session_dir.joinpath("Session 04.md")
        latest_session.write_text("test session", newline="\n")

        result = tmp_campaign.bump_planning_files()

        expected_plot = tmp_campaign.plot_dir.joinpath("Plot 04.md")
        assert result["session"] == latest_session
        assert result["plot"] == expected_plot

    def test_jumps_big_gap(self, tmp_campaign):
        populate(tmp_campaign, plots = 1, sessions = 5)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 5

class TestWithMatchingIndexes:
    def test_creates_new_plot_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.plot_dir.joinpath("Plot 04.md").exists()

    def test_updates_saved_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_plot_index == 4

    def test_creates_new_session_file(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.session_dir.joinpath("Session 04.md").exists()

    def test_updates_saved_session_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.latest_session_index == 4

    def test_returns_both_files(self, tmp_campaign):
        populate(tmp_campaign, plots = 3, sessions = 3)

        result = tmp_campaign.bump_planning_files()

        expected_plot = tmp_campaign.plot_dir.joinpath("Plot 04.md")
        expected_session = tmp_campaign.session_dir.joinpath("Session 04.md")
        assert result["plot"] == expected_plot
        assert result["session"] == expected_session

class TestWithMissingSession:
    def test_does_not_increment(self, tmp_campaign):
        populate(tmp_campaign, plots = 2)

        result = tmp_campaign.bump_planning_files()

        expected_plot = tmp_campaign.plot_dir.joinpath("Plot 02.md")
        assert result["plot"] == expected_plot

    def test_uses_plot_index(self, tmp_campaign):
        populate(tmp_campaign, plots = 2)

        result = tmp_campaign.bump_planning_files()

        expected_session = tmp_campaign.session_dir.joinpath("Session 02.md")
        assert result["session"] == expected_session

class TestAdditionalFiles:
    def test_creates_additional_plot_in_plot_dir(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({
            "plot": {
                "additional_files": [
                    {"filename_pattern": "Test ((NN)).md", "file_contents": "test"}
                ]
            }
        })

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.plot_dir.joinpath("Test 01.md").exists()

    def test_creates_additional_session_in_session_dir(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({
            "session": {
                "additional_files": [
                    {"filename_pattern": "Test ((NN)).md", "file_contents": "test"}
                ]
            }
        })

        tmp_campaign.bump_planning_files()

        assert tmp_campaign.session_dir.joinpath("Test 01.md").exists()

    def test_inserts_contents(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({
            "plot": {
                "additional_files": [
                    {"filename_pattern": "Test ((NN)).md", "file_contents": "test"}
                ]
            }
        })

        tmp_campaign.bump_planning_files()

        outfile = tmp_campaign.plot_dir.joinpath("Test 01.md")
        assert outfile.read_text() == "test"
