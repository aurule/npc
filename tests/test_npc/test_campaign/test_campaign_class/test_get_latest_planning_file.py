import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

def test_throws_on_bad_key(tmp_campaign):
    with pytest.raises(KeyError):
        tmp_campaign.get_latest_planning_file("nope")

class TestWithNoFiles:
    @pytest.mark.parametrize("key", ["plot", "session"])
    def test_returns_none(self, tmp_campaign, key):
        result = tmp_campaign.get_latest_planning_file(key)

        assert result is None

class TestWithOneUsefulFile:
    @pytest.mark.parametrize("key, path", [("plot", ("Plot", "Plot 05.md")), ("session", ("Session History", "Session 05.md"))])
    def test_returns_file_path(self, tmp_campaign, key, path):
        root = tmp_campaign.root
        root.joinpath(*path).touch()

        result = tmp_campaign.get_latest_planning_file(key)

        assert result == root.joinpath(*path)

class TestWithManyFiles:
    @pytest.mark.parametrize("key, path, files", [
        ("plot", "Plot", ["Plot 01.md", "Plot 02.md", "Plot 03.md"]),
        ("session", "Session History", ["Session 01.md", "Session 02.md", "Session 03.md"])
        ])
    def test_returns_file_path(self, tmp_campaign, key, path, files):
        root = tmp_campaign.root
        for filename in files:
            root.joinpath(path, filename).touch()

        result = tmp_campaign.get_latest_planning_file(key)

        assert result == root / path / files[-1]

    @pytest.mark.parametrize("key, path, files", [
        ("plot", "Plot", ["Plot 01.md", "Plot 02.md", "Plot 03.md"]),
        ("session", "Session History", ["Session 01.md", "Session 02.md", "Session 03.md"])
        ])
    def test_ignores_other_files(self, tmp_campaign, key, path, files):
        root = tmp_campaign.root
        for filename in files:
            root.joinpath(path, filename).touch()
        root.joinpath(path, "Extra 04.md").touch()

        result = tmp_campaign.get_latest_planning_file(key)

        assert result == root / path / files[-1]
