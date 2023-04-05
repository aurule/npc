from npc.settings import PlanningFilename

def test_replaces_pattern_with_num():
    pf = PlanningFilename("Session ((N)).md")

    result = pf.for_index(152)

    assert result == "Session 152.md"

def test_pads_number_to_width():
    pf = PlanningFilename("Session ((NNN)).md")

    result = pf.for_index(5)

    assert result == "Session 005.md"

def test_returns_name_unchanged_without_placeholder():
    pf = PlanningFilename("Session.md")

    result = pf.for_index(5)

    assert result == "Session.md"
