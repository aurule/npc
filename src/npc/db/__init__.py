from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from ..util import Singleton

class DB(metaclass=Singleton):
    """Internal database class

    Since this class uses Singleton as its metaclass, you can pass the special clearSingleton=True parameter
    if you want to create a standalone DB instance instead of using the normal singleton instance. This is
    mainly meant for ease of writing tests.
    """
    def __init__(self):
        self.engine = create_engine("sqlite://")
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
