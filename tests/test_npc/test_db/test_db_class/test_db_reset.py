import pytest

from sqlalchemy import MetaData, text

from npc.db.database import DB

@pytest.mark.xfail(reason="Fails in full suite, not individually or small suite")
def test_removes_records():
    db = DB(clearSingleton=True)
    metadata = MetaData()
    metadata.reflect(db.engine)
    with db.session() as session:
        query = text("INSERT INTO characters (realname, type_key, nolint, sticky, delist) VALUES ('tester', 'default', False, False, False)")
        session.execute(query)
    with db.session() as session:
        query = text("SELECT id FROM characters LIMIT 1")
        result = session.scalar(query)

        assert result

    db.reset()

    with db.session() as session:
        query = text("SELECT id FROM characters LIMIT 1")
        result = session.scalar(query)

        assert not result
