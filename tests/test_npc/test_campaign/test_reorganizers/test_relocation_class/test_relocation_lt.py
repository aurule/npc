from npc.campaign.reorganizers.relocation_class import Relocation

def test_true_when_currpath_eq_other_ideal():
    reloc1 = Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/second.txt")
    reloc2 = Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "/test/whynot.txt")

    assert reloc2 < reloc1

def test_false_when_currpath_neq_other_ideal():
    reloc1 = Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/first.txt")
    reloc2 = Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "/test/whynot.txt")

    assert not reloc2 < reloc1
