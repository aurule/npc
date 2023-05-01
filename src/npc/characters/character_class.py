from pathlib import Path
from sqlalchemy import String, Text
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
    """

    # Names of tags which are represented by properties on the Character object, instead of as associated Tags
    MAPPED_TAGS = ["realname", "delist", "nolint", "sticky", "type"]

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    delist: Mapped[bool]
    desc: Mapped[Optional[str]] = mapped_column(Text)
    file_body: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(String(1024))
    mnemonic: Mapped[Optional[str]] = mapped_column(String(1024))
    realname: Mapped[str] = mapped_column(String(1024))
    nolint: Mapped[bool]
    sticky: Mapped[bool]
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
        return self.realname
