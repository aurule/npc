import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

def test_throws_on_bad_key():
    settings = Settings()
    with pytest.raises(KeyError):
        settings.get_latest_planning_index("nope")

class TestWithNoCampaignDir:
    @pytest.mark.parametrize("key", ["plot", "session"])
    def test_returns_saved_index(self, key):
        settings = Settings()

        result = settings.get_latest_planning_index(key)

        assert result == 0

class TestWithNoFiles:
    @pytest.mark.parametrize("key", ["plot", "session"])
    def test_returns_saved_index(self, tmp_campaign, key):
        tmp_path, settings = tmp_campaign

        result = settings.get_latest_planning_index(key)

        assert result == 0

class TestWithOneUsefulFile:
    @pytest.mark.parametrize("key, path", [("plot", ("Plot", "Plot 05.md")), ("session", ("Session History", "Session 05.md"))])
    def test_returns_file_index(self, tmp_campaign, key, path):
        tmp_path, settings = tmp_campaign
        tmp_path.joinpath(*path).touch()

        result = settings.get_latest_planning_index(key)

        assert result == 5

    @pytest.mark.parametrize("key, path", [("plot", ("Plot", "Plot 05.md")), ("session", ("Session History", "Session 05.md"))])
    def test_updates_saved_index(self, tmp_campaign, key, path):
        tmp_path, settings = tmp_campaign
        tmp_path.joinpath(*path).touch()

        settings.get_latest_planning_index(key)

        assert settings.get(f"campaign.{key}.latest_index") == 5

class TestWithManyFiles:
    @pytest.mark.parametrize("key, path, files", [
        ("plot", "Plot", ["Plot 01.md", "Plot 02.md", "Plot 03.md"]),
        ("session", "Session History", ["Session 01.md", "Session 02.md", "Session 03.md"])
        ])
    def test_returns_highest_index(self, tmp_campaign, key, path, files):
        tmp_path, settings = tmp_campaign
        for filename in files:
            tmp_path.joinpath(path, filename).touch()

        result = settings.get_latest_planning_index(key)

        assert result == 3

    @pytest.mark.parametrize("key, path, files", [
        ("plot", "Plot", ["Plot 01.md", "Plot 02.md", "Plot 03.md"]),
        ("session", "Session History", ["Session 01.md", "Session 02.md", "Session 03.md"])
        ])
    def test_updates_saved_index(self, tmp_campaign, key, path, files):
        tmp_path, settings = tmp_campaign
        for filename in files:
            tmp_path.joinpath(path, filename).touch()

        settings.get_latest_planning_index(key)

        assert settings.get(f"campaign.{key}.latest_index") == 3

    @pytest.mark.parametrize("key, path, files", [
        ("plot", "Plot", ["Plot 01.md", "Plot 02.md", "Plot 03.md"]),
        ("session", "Session History", ["Session 01.md", "Session 02.md", "Session 03.md"])
        ])
    def test_ignores_other_files(self, tmp_campaign, key, path, files):
        tmp_path, settings = tmp_campaign
        for filename in files:
            tmp_path.joinpath(path, filename).touch()
        tmp_path.joinpath(path, "Extra 04.md").touch()

        result = settings.get_latest_planning_index(key)

        assert result == 3
