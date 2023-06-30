from npc.db.custom_functions import first_word

def test_gets_last_of_many():
    data = "one two three"

    result = first_word(data)

    assert result == "one"

def test_gets_singleton():
    data = "one"

    result = first_word(data)

    assert result == "one"
