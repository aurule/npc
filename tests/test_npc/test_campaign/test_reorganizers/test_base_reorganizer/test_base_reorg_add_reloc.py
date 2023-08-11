from npc.campaign.reorganizers import BaseReorganizer

def test_adds_relocation():
    reorganizer = BaseReorganizer()

    reorganizer.add_relocation(1, "hi", "hello")

    assert len(reorganizer.relocations) == 1
