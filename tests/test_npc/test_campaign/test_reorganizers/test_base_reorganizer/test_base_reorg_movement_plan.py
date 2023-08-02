from npc.campaign.reorganizers import BaseReorganizer

from npc.campaign.reorganizers.relocation_class import Relocation

def test_empty_without_paths():
    reorganizer = BaseReorganizer()

    result = reorganizer.make_movement_plan()

    assert result == []

def test_empty_without_changes():
    reorganizer = BaseReorganizer()
    reorganizer.relocations = [
        Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/first.txt"),
        Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "/test/second.txt"),
    ]

    result = reorganizer.make_movement_plan()

    assert result == []

def test_moves_in_safe_order():
    # when path 1 has the ideal path matching path 2's current path, path 2 should go first
    reorganizer = BaseReorganizer()
    rp1 = Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "/test/second.txt")
    rp2 = Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "/test/whynot.txt")
    reorganizer.relocations = [rp1, rp2]

    result = reorganizer.make_movement_plan()

    assert result == [rp2, rp1]
