import pytest

from npc.campaign.reorganizers import BaseReorganizer

def test_throws_error():
    reorganizer = BaseReorganizer()

    with pytest.raises(NotImplementedError):
        reorganizer.gather_paths()
