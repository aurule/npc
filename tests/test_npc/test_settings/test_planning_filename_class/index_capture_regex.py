from npc.settings import PlanningFilename

def test_substitues_regex():
    pf = PlanningFilename("Session ((NNN)).md")

    assert pf.index_capture_regex == "Session (?P<number>\\d+)"

def test_does_nothing_without_match():
    pf = PlanningFilename("Session.md")

    assert pf.index_capture_regex == "Session.md"
