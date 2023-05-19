from pathlib import Path
from sqlalchemy import String, Text, select, Select, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional
from .taggable_interface import Taggable
from .tag_class import Tag

from ..db import BaseModel

@Taggable.register
class Character(BaseModel):
    """Class representing a single character

    Holds tag and file body data from a character file, backed by a database for ease of use. The database
    is merely a cache, though: the file on disk is the source of truth.

    Handles validating and changing individual characters, as well as fetching specific tag values

    Required Attributes:
        id          int     auto
        delist      bool    default False
        realname    str
        nolint      bool    default False
        sticky      bool    default False
        type_key    str
    Optional Attributes
        desc        str
        file_body   str
        file_loc    str
        mnemonic    str
        tags        rel     Tag
    """

    # Names of tags which are represented by properties on the Character object, instead of as associated Tags
    MAPPED_TAGS = ["realname", "delist", "nolint", "sticky", "type"]

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    delist: Mapped[bool] = mapped_column(Boolean, default=False)
    desc: Mapped[Optional[str]] = mapped_column(Text)
    file_body: Mapped[Optional[str]] = mapped_column(Text)
    file_loc: Mapped[Optional[str]] = mapped_column(String(1024))
    mnemonic: Mapped[Optional[str]] = mapped_column(String(1024))
    realname: Mapped[str] = mapped_column(String(1024))
    nolint: Mapped[bool] = mapped_column(Boolean, default=False)
    sticky: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[List["Tag"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan"
    )
    type_key: Mapped[str] = mapped_column(String(128))

    def __repr__(self) -> str:
        return f"Character(id={self.id!r}, realname={self.realname!r})"

    def accepts_tag(self, tag_name: str) -> bool:
        """Indicate that Character objects accept all tags

        Args:
            tag_name (str): Tag name to test

        Returns:
            bool: True. Character objects accept all tags.
        """
        return True

    def add_tag(self, tag: Tag):
        """Add the tag to our tags list

        Adds the tag to our tags property.

        Args:
            tag (Tag): Tag to add
        """
        self.tags.append(tag)

    @property
    def name(self) -> str:
        """Get the canonical name of this character

        Used when adding tags.

        Returns:
            str: The realname of this character
        """
        return self.realname

    @property
    def file_path(self) -> Path:
        """Get the character's file location as a Path

        Returns:
            Path: Path object representing the character's file_loc property
        """
        return Path(self.file_loc)

    @file_path.setter
    def file_path(self, new_path: Path):
        """Set the character's file location from a Path

        Args:
            new_path (Path): Path to use for the new location
        """
        self.file_loc = str(new_path)

    def tag_value_query(self, *names: str) -> Select:
        """Create a database query to get values for our tags

        Builds a DB query for the named tags, scoped to this character. This query only returns tag values.

        Args:
            names (Tuple[str]): Tag names to include in the query

        Returns:
            Select: Select object for a tag value query
        """
        return select(Tag.value) \
            .where(Tag.name.in_(names)) \
            .filter(Tag.character_id == self.id) \
            .order_by(Tag.id)
