from npc.db.query_builders import CharacterListerQueryBuilder

def test_queries_realname():
    builder = CharacterListerQueryBuilder()

    builder.apply_full_name_partial("test")

    assert "realname AS test" in str(builder.query)

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_full_name_partial("test")

    assert "test" in str(builder.query)
