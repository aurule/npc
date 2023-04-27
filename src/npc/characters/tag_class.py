from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional

from ..db import BaseModel

class Tag(BaseModel):
    """Class representing a single tag value

    Holds a single value for a single tag belonging to a single character.
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[Optional["Character"]] = relationship(back_populates="tags")
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("characters.id"))
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[Optional[str]] = mapped_column(Text)
    subtags: Mapped[Optional[List["Tag"]]] = relationship(
        back_populates="parent_tag",
        cascade="all, delete-orphan",
    )
    parent_tag: Mapped[Optional["Tag"]] = relationship()
    parent_tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tags.id"))

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r}, value={self.value!r})"
