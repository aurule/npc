from npc.db.query_builders import CharacterListerQueryBuilder

def test_applies_first_word_func():
    builder = CharacterListerQueryBuilder()

    builder.apply_first_name_partial("test")

    assert "first_word(characters.realname)" in str(builder.query)

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_first_name_partial("test")

    assert "test" in str(builder.query)
