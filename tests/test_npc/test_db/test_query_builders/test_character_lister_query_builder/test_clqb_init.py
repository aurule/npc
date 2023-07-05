from npc.db.query_builders import CharacterListerQueryBuilder

def test_excludes_delist():
    builder = CharacterListerQueryBuilder()

    assert "delist = false" in str(builder.query)
