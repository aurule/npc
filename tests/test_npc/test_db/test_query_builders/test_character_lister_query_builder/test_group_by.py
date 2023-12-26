from npc.db.query_builders import CharacterListerQueryBuilder

def test_records_group_criterion():
    builder = CharacterListerQueryBuilder()

    builder.group_by("org")

    assert "org" in builder.grouped_by

def test_increments_index_last():
    builder = CharacterListerQueryBuilder()

    builder.group_by("org")

    assert "group0" in str(builder.query)
