from npc.campaign.reorganizers import BaseReorganizer

from npc.campaign.reorganizers.relocation_class import Relocation

def test_returns_empty_with_no_paths():
    reorganizer = BaseReorganizer()

    result = reorganizer.check_conflicts()

    assert result == []

def test_returns_empty_without_conflicts():
    reorganizer = BaseReorganizer()
    reorganizer.relocations = [
        Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "test/first - first.txt"),
        Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "test/second - second.txt"),
    ]

    result = reorganizer.check_conflicts()

    assert result == []

def test_returns_conflict_message():
    reorganizer = BaseReorganizer()
    reorganizer.relocations = [
        Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "test/first - first.txt"),
        Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "test/first - first.txt"),
    ]

    result = reorganizer.check_conflicts()

    assert "first - first.txt" in result[0]

def test_returns_one_conflict_message_per_path():
    reorganizer = BaseReorganizer()
    reorganizer.relocations = [
        Relocation(id = 1, current_path = "/test/first.txt", ideal_path = "test/first - first.txt"),
        Relocation(id = 2, current_path = "/test/second.txt", ideal_path = "test/first - first.txt"),
        Relocation(id = 3, current_path = "/test/third.txt", ideal_path = "test/first - first.txt"),
    ]

    result = reorganizer.check_conflicts()

    assert len(result) == 1
