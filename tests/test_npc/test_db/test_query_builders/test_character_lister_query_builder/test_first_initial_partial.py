from npc.db.query_builders import CharacterListerQueryBuilder

def test_examines_name_first_char():
    builder = CharacterListerQueryBuilder()

    builder.apply_first_initial_partial("test")

    assert "substr(characters.realname" in str(builder.query)

def test_includes_label():
    builder = CharacterListerQueryBuilder()

    builder.apply_first_initial_partial("test")

    assert "test" in str(builder.query)
