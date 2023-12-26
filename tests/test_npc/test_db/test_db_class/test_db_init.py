from sqlalchemy import MetaData, text

from npc.db.database import DB

def test_creates_tables():
    db = DB(clearSingleton=True)
    metadata = MetaData()
    metadata.reflect(db.engine)

    assert "characters" in metadata.tables

def test_injects_first_word_func():
    db = DB(clearSingleton=True)

    with db.session() as session:
        query = text("SELECT first_word('one two three')")
        result = session.scalar(query)
        assert result == 'one'

def test_injects_last_word_func():
    db = DB(clearSingleton=True)

    with db.session() as session:
        query = text("SELECT last_word('one two three')")
        result = session.scalar(query)
        assert result == 'three'
