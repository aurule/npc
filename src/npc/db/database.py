from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session

from . import custom_functions
from npc.util import Singleton

class DB(metaclass=Singleton):
    """Internal database class

    Since this class uses Singleton as its metaclass, you can pass the special clearSingleton=True parameter
    if you want to create a standalone DB instance instead of using the normal singleton instance. This is
    mainly meant for ease of writing tests.
    """
    def __init__(self):
        self.engine = create_engine("sqlite://")

        @event.listens_for(self.engine, "connect")
        def inject_functions(conn, rec):
            conn.create_function("last_word", 1, custom_functions.last_word)
            conn.create_function("first_word", 1, custom_functions.first_word)

        BaseModel.metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        """Get a session for this database instance

        Yields a session that is bound to this database

        Yields:
            A session instance that can be used to modify the database in a transaction.
            Session
        """
        yield Session(self.engine)

class BaseModel(DeclarativeBase):
    """Base model for creating sqlalchemy classes

    All sqlalchemy model classes should extend this module as their parent
    """
