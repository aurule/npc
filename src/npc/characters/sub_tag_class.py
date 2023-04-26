from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List

from ..db import BaseModel

class SubTag(BaseModel):
    """Class representing a single subtag value

    Holds a single value for a subtag, related to a parent tag
    """

    __tablename__ = "subtags"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped["Tag"] = relationship(back_populates: "subtags")
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(Text)
