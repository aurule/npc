from npc.campaign.reorganizers.relocation_class import Relocation
from tests.fixtures import ProgressCounter

from npc.campaign.reorganizers import BaseReorganizer

def test_handles_renames(tmp_path):
    curr = tmp_path / "first.txt"
    curr.touch()
    ideal = tmp_path / "first - first.txt"
    plan = [Relocation(id = 1, current_path = curr, ideal_path = ideal)]
    reorganizer = BaseReorganizer()

    reorganizer.execute_movement_plan(plan)

    assert ideal.exists()

def test_handles_move_to_existing_dir(tmp_path):
    curr = tmp_path / "first.txt"
    curr.touch()
    olddir = tmp_path / "olddir"
    olddir.mkdir()
    ideal = olddir / "first - first.txt"
    plan = [Relocation(id = 1, current_path = curr, ideal_path = ideal)]
    reorganizer = BaseReorganizer()

    reorganizer.execute_movement_plan(plan)

    assert ideal.exists()

def test_handles_move_to_new_dir(tmp_path):
    curr = tmp_path / "first.txt"
    curr.touch()
    newdir = tmp_path / "newdir"
    ideal = newdir / "first - first.txt"
    plan = [Relocation(id = 1, current_path = curr, ideal_path = ideal)]
    reorganizer = BaseReorganizer()

    reorganizer.execute_movement_plan(plan)

    assert ideal.exists()

def test_updates_progress(tmp_path):
    curr = tmp_path / "first.txt"
    curr.touch()
    ideal = tmp_path / "first - first.txt"
    plan = [Relocation(id = 1, current_path = curr, ideal_path = ideal)]
    reorganizer = BaseReorganizer()
    counter = ProgressCounter()

    reorganizer.execute_movement_plan(plan, counter.progress)

    assert counter.count == 1
