from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from ..util import Singleton

class DB(Singleton):
    def __init__(self):
        self.engine = create_engine("sqlite://")
        BaseModel.metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        yield Session(self.engine)

class BaseModel(DeclarativeBase):
    pass
