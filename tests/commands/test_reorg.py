import npc
import pytest
from pathlib import Path

def do_reorg(commit=True, **kwargs):
    return npc.commands.reorg('Characters', commit=commit, **kwargs)

@pytest.mark.parametrize('new_path', [
    Path('Fetches/Foermer Loover.nwod'), # in the wrong type folder
    Path('Goblins/Natwick Hardingle.nwod'), # already in the right folder
    Path('Humans/Alpha Mann.nwod'), # not in a type folder
])
def test_move_by_type(campaign, new_path):
    campaign.populate_from_fixture_dir('reorg', 'by_type')
    result = do_reorg()
    assert result
    character = campaign.get_character(new_path)
    assert character.exists()

@pytest.mark.parametrize('new_path', [
    Path('Goblins/Market/Marcy Marketto.nwod'),
    Path('Humans/Mafia/Mafia Mann.nwod'),
    Path('Humans/Police/Popo Panckett.nwod'),
])
def test_move_by_group(campaign, new_path):
    """Reorg should move non-changeling characters to nested group directories
    under their type directory."""

    campaign.populate_from_fixture_dir('reorg', 'by_group')
    result = do_reorg(verbose=True)
    print(result.printables)
    character = campaign.get_character(new_path)
    assert character.exists()

def test_partial_tree(campaign):
    """Should not choke when ideal dirs don't exist"""

    campaign.populate_from_fixture_dir('reorg', 'partial_tree')
    result = do_reorg()
    assert result.success
    character = campaign.get_character(Path('Humans/JJ.nwod'))
    assert character.exists()

def test_commit(campaign):
    campaign.populate_from_fixture_dir('reorg', 'by_type')
    do_reorg(commit=False)
    character = campaign.get_character('Alpha Mann.nwod')
    assert character.exists()

class TestPurge:
    def test_removes_directories(self, campaign):
        """Removes empty directories with purge option"""

        campaign.populate_from_fixture_dir('reorg', 'purge_removes')
        result = do_reorg(purge=True)
        assert result.success
        fetches_folder = campaign.get_character(Path('Fetches'))
        assert not fetches_folder.exists()

    def test_preserves_directories(self, campaign):
        """Does not remove empty directories without purge option"""

        campaign.populate_from_fixture_dir('reorg', 'no_purge_preserves')
        result = do_reorg()
        assert result.success
        humans_folder = campaign.get_character(Path('Humans'))
        assert humans_folder.exists()

class TestChangeling:
    @pytest.mark.parametrize('new_path', [
        Path('Changelings/Autumn/Alice Autumn.nwod'),
        Path('Changelings/Spring/Sally Spring.nwod'),
        Path('Changelings/Summer/Samantha Summer.nwod'),
        Path('Changelings/Winter/Wanda Winter.nwod'),
    ])
    def test_move_by_court(self, campaign, new_path):
        campaign.populate_from_fixture_dir('reorg', 'changeling_courts')
        do_reorg()
        character = campaign.get_character(new_path)
        assert character.exists()

    def test_move_courtless(self, campaign):
        campaign.populate_from_fixture_dir('reorg', 'changeling_courtless')
        do_reorg()
        character = campaign.get_character(Path('Changelings/Courtless/Connie Courtless.nwod'),)
        assert character.exists()

    @pytest.mark.parametrize('new_path', [
        Path('Changelings/Summer/Hound Tribunal/Samantha Summer.nwod'),
        Path('Changelings/Courtless/Vagrants/Connie Courtless.nwod'),
    ])
    def test_move_by_group(self, campaign, new_path):
        """Changeling characters should be moved to nested group directories
        within their type and court."""

        campaign.populate_from_fixture_dir('reorg', 'changeling_group')
        do_reorg()
        character = campaign.get_character(new_path)
        assert character.exists()
