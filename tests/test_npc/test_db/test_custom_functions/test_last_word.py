from npc.db.custom_functions import last_word

def test_gets_last_of_many():
    data = "one two three"

    result = last_word(data)

    assert result == "three"

def test_gets_singleton():
    data = "one"

    result = last_word(data)

    assert result == "one"
