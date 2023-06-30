from npc.db.query_builders import CharacterListerQueryBuilder

def test_includes_all_characters():
    builder = CharacterListerQueryBuilder()

    builder.apply_tag_partial("org", "test")

    assert "LEFT OUTER JOIN" in str(builder.query)

def test_limits_to_tag_name():
    builder = CharacterListerQueryBuilder()

    builder.apply_tag_partial("org", "test")

    assert "tags_1.name = :name_1" in str(builder.query)

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_tag_partial("org", "test")

    assert "test" in str(builder.query)
