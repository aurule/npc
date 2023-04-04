from tests.fixtures import tmp_campaign

from npc.settings import Settings

def test_throws_on_bad_key():
    pass

class TestWithNoCampaignDir:
    def test_returns_saved_index(self):
        pass

class TestWithOneUsefulFile:
    def test_returns_file_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        pass

    def test_updates_saved_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        pass

class TestWithManyFiles:
    def test_returns_highest_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        pass

    def test_updates_saved_index(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        pass

    def test_ignores_other_files(self, tmp_campaign):
        tmp_path, settings = tmp_campaign
        pass
