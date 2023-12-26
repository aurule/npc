from sqlalchemy.orm import Session

from npc.db import DB

def test_yields_session_for_engine():
    db = DB(clearSingleton=True)

    with db.session() as s:
        assert isinstance(s, Session)
        assert s.get_bind() == db.engine
