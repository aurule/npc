from npc.settings import PlanningFilename

def test_returns_zero_without_match():
    pf = PlanningFilename("Session.md")

    assert pf.index_width == 0

def test_returns_count_of_Ns():
    pf = PlanningFilename("Session ((NNN)).md")

    assert pf.index_width == 3
