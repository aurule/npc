import npc
import pytest
import os

# tests
# moves changelings to right court dir, when given
# moves changelings to Courtless dir, when court not given
# moves changeling to nested groups dir under type/court, when given

@pytest.mark.parametrize('new_path', [
    os.path.join('Fetches', 'Foermer Loover.nwod'), # in the wrong type folder
    os.path.join('Goblins', 'Natwick Hardingle.nwod'), # already in the right folder
    os.path.join('Humans', 'Alpha Mann.nwod'), # not in a type folder
])
def test_move_by_type(campaign, new_path):
    campaign.populate_from_fixture_dir(['reorg', 'by_type'])
    result = npc.commands.reorg('Characters')
    assert result.success
    character = campaign.get_character(new_path)
    assert character.check()

@pytest.mark.parametrize('new_path', [
    os.path.join('Goblins', 'Market', 'Marcy Marketto.nwod'),
    os.path.join('Humans', 'Mafia', 'Mafia Mann.nwod'),
    os.path.join('Humans', 'Police', 'Popo Panckett.nwod'),
])
def test_move_by_group(campaign, new_path):
    """Reorg should move non-changeling characters to nested group directories
    under their type directory."""

    campaign.populate_from_fixture_dir(['reorg', 'by_group'])
    npc.commands.reorg('Characters')
    character = campaign.get_character(new_path)
    assert character.check()

@pytest.mark.parametrize('new_path', [
    os.path.join('Humans', 'Foreign', 'Manny Mafioso.nwod'),
    os.path.join('Humans', 'Mafia', 'Mafia Mann.nwod'),
    os.path.join('Humans', 'Police', 'Popo Panckett.nwod'),
])
def test_move_by_foreign(campaign, new_path):
    """Reorg should move foreigners to Foreign under their type or group."""

    campaign.populate_from_fixture_dir(['reorg', 'by_foreign'])
    npc.commands.reorg('Characters')
    character = campaign.get_character(new_path)
    assert character.check()

def test_partial_tree(campaign):
    """Should not choke when ideal dirs don't exist"""

    campaign.populate_from_fixture_dir(['reorg', 'partial_tree'])
    result = npc.commands.reorg('Characters')
    assert result.success
    character = campaign.get_character(os.path.join('Humans', 'JJ.nwod'))
    assert character.check()

def test_dry_run(campaign):
    campaign.populate_from_fixture_dir(['reorg', 'by_type'])
    npc.commands.reorg('Characters', dry=True)
    character = campaign.get_character('Alpha Mann.nwod')
    assert character.check()

class TestPurge:
    def test_removes_directories(self, campaign):
        """Removes empty directories with purge option"""

        campaign.populate_from_fixture_dir(['reorg', 'purge_removes'])
        result = npc.commands.reorg('Characters', purge=True)
        assert result.success
        fetches_folder = campaign.get_character(os.path.join('Fetches'))
        assert not fetches_folder.check()

    def test_preserves_directories(self, campaign):
        """Does not remove empty directories without purge option"""

        campaign.populate_from_fixture_dir(['reorg', 'no_purge_preserves'])
        result = npc.commands.reorg('Characters')
        assert result.success
        humans_folder = campaign.get_character(os.path.join('Humans'))
        assert humans_folder.check()

class TestChangeling:
    @pytest.mark.parametrize('new_path', [
        os.path.join('Changelings', 'Autumn', 'Alice Autumn.nwod'),
        os.path.join('Changelings', 'Spring', 'Sally Spring.nwod'),
        os.path.join('Changelings', 'Summer', 'Samantha Summer.nwod'),
        os.path.join('Changelings', 'Winter', 'Wanda Winter.nwod'),
    ])
    def test_move_by_court(self, campaign, new_path):
        campaign.populate_from_fixture_dir(['reorg', 'changeling_courts'])
        npc.commands.reorg('Characters')
        character = campaign.get_character(new_path)
        assert character.check()

    def test_move_courtless(self, campaign):
        campaign.populate_from_fixture_dir(['reorg', 'changeling_courtless'])
        npc.commands.reorg('Characters')
        character = campaign.get_character(os.path.join('Changelings', 'Courtless', 'Connie Courtless.nwod'),)
        assert character.check()

    @pytest.mark.parametrize('new_path', [
        os.path.join('Changelings', 'Summer', 'Hound Tribunal', 'Samantha Summer.nwod'),
        os.path.join('Changelings', 'Courtless', 'Vagrants', 'Connie Courtless.nwod'),
    ])
    def test_move_by_group(self, campaign, new_path):
        """Changeling characters should be moved to nested group directories
        within their type and court."""

        campaign.populate_from_fixture_dir(['reorg', 'changeling_group'])
        npc.commands.reorg('Characters')
        character = campaign.get_character(new_path)
        assert character.check()
