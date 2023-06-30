from npc.db.query_builders import CharacterListerQueryBuilder

def test_queries_type_key():
    builder = CharacterListerQueryBuilder()

    builder.apply_type_partial("test")

    assert "type_key AS test" in str(builder.query)

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_type_partial("test")

    assert "test" in str(builder.query)
