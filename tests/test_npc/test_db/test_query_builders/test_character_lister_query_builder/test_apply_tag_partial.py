from npc.db.query_builders import CharacterListerQueryBuilder

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_tag_partial("org", "test")

    assert "test" in str(builder.query)
