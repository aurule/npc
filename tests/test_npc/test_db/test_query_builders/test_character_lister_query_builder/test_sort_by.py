from npc.db.query_builders import CharacterListerQueryBuilder

def test_records_group_criterion():
    builder = CharacterListerQueryBuilder()

    builder.sort_by("org")

    assert "org" in builder.sorted_by

def test_increments_index_last():
    builder = CharacterListerQueryBuilder()

    builder.sort_by("org")

    assert "sort0" in str(builder.query)
