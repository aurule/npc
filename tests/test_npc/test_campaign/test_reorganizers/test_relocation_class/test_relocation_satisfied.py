from npc.campaign.reorganizers.relocation_class import Relocation

def test_true_when_currpath_eq_ideal():
    reloc = Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/first.txt")

    assert reloc.satisfied

def test_false_when_currpath_neq_ideal():
    reloc = Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/second.txt")

    assert not reloc.satisfied
