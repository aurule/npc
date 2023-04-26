from pathlib import Path
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List

from ..db import BaseModel

class Character(BaseModel):
    """Class representing a single character

    Holds tag and file body data from a character file, backed by a database for ease of use. The database
    is merely a cache, though: the file on disk is the source of truth.

    Handles validating and changing individual characters, as well as fetching specific tag values
    """

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[List["Tag"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan"
    )
    file_body: Mapped[str] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(String(1024))

    def __init__(self, tags: dict = {}, *, id: int = None, file_body: str = None, file_path: Path = None):
        # create tag records from tags
        # populate id, file body, and file path
        pass

    # type_key prop
    # name prop
    # description prop
