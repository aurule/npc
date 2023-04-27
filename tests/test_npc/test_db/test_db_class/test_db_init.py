from sqlalchemy import MetaData

from npc.db import DB

def test_creates_tables():
    db = DB(clearSingleton=True)
    metadata = MetaData()
    metadata.reflect(db.engine)

    assert "characters" in metadata.tables
