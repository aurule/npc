from npc.campaign.reorganizers import BaseReorganizer

def test_initializes_empty_paths():
    reorganizer = BaseReorganizer()

    assert reorganizer.ideal_paths == []
