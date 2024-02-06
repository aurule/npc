from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional, Union
from dataclasses import dataclass

from .taggable_interface import Taggable
from npc.db import BaseModel

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
        parent_tag_id   int
        hidden          str     [None, "all", "one"]
        sequence        int     0
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[Optional["Character"]] = relationship(back_populates="tags") # noqa: F821
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("characters.id"))
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[Optional[str]] = mapped_column(Text)
    subtags: Mapped[Optional[List["Tag"]]] = relationship(
        cascade="all, delete-orphan",
    )
    parent_tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tags.id"))
    hidden: Mapped[Optional[str]] = mapped_column(String(3))
    sequence: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r}, value={self.value!r}, hidden={self.hidden is not None})"

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

    def emit(self) -> str:
        """Generate a parseable representation of this tag and its subtags

        The value is only included if set and non-falsey.
            @flag
            @tag value
            @subtag new value
            @subtag other value

        Returns:
            str: Parseable version of the tag and its subtags
        """
        out = f"@{self.name}"
        if self.value:
            out += (f" {self.value}")

        lines = [out] + [subtag.emit() for subtag in self.subtags]

        return "\n".join(lines)

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
