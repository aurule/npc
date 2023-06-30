from npc.db.query_builders import CharacterListerQueryBuilder

def test_uses_attr_partial():
    builder = CharacterListerQueryBuilder()

    builder.pick_partial("type", "test")

    assert "type_key AS test" in str(builder.query)

def test_falls_back_on_tag_partial():
    builder = CharacterListerQueryBuilder()

    builder.pick_partial("surprise", "test")

    assert "tags_1" in str(builder.query)
