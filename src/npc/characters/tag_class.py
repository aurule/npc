from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List

from ..db import BaseModel

class Tag(BaseModel):
    """Class representing a single tag value

    Holds a single value for a single tag belonging to a single character.
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped["Character"] = relationship(back_populates: "tags")
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(Text)
    subtags: Mapped[List["SubTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )
