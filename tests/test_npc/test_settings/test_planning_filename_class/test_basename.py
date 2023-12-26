from npc.settings import PlanningFilename

def test_excludes_suffix():
    pf = PlanningFilename("Session ((NNN)).md")

    assert pf.basename == "Session ((NNN))"
