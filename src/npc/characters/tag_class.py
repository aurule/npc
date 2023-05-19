from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional, Union
from dataclasses import dataclass

from .taggable_interface import Taggable
from ..db import BaseModel

@Taggable.register
class Tag(BaseModel):
    """Class representing a single tag value

    Holds a single value for a single tag belonging to a single character.

    Required Attributes:
        id              int (auto)
        name            str
    Optional Attributes:
        character       rel     Character
        character_id    int
        value           str
        subtags         rel     Tag
        parent_tag      rel     Tag
        parent_tag_id   int
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

    def accepts_tag(self, tag_name: str) -> bool:
        """Get whether this object accepts the named tag as a subtag

        Args:
            tag_name (str): Name of the tag to test

        Returns:
            bool: True if this tag allows subtags, and the named tag appears in the list of subtags in our spec
        """
        return self.spec.subtags and tag_name in self.spec.subtags

    def add_tag(self, tag):
        """Add the given tag to our subtags

        Args:
            tag (Tag): The tag to add
        """
        self.subtags.append(tag)

@dataclass
class RawTag():
    """Class for passing raw tag data

    This is little more than a fancy tuple. It should be used instead of a database-backed Tag object when you
    just need to pass around tag name/value pairs.

    Attributes:
        name: Name of the tag
        value: Value of the tag
    """
    name: str
    value: Union[str, int]
