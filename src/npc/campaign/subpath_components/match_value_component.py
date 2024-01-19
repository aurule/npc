from sqlalchemy import Select
from pathlib import Path

from .base_component import BaseSubpathComponent
from npc.characters import Character, Tag
from npc.db import DB, character_repository

class MatchValueComponent(BaseSubpathComponent):
    """Match Value subpath component

    This component returns a static string if the first value found within the specified tags
    matches the string in `equals`.

    Attributes:
        SELECTOR: The selector string
    """

    SELECTOR = "match_value"

    def __init__(self, db: DB, spec: dict, only_existing: bool = False):
        super().__init__(db, spec, only_existing)

        self.tag_names = self.from_spec("tags")
        self._value = self.from_spec("value")
        self.target = self.from_spec("equals")

    def tag_value(self, character: Character, current_path: Path) -> str:
        """Get the value of this component

        Return the configured static value if the first value of the first existing tag in
        tag_names matches the value in equals.

        Args:
            character (Character): Character to test
            current_path (Path): Current working path (ignored)

        Returns:
            str: A new directory name, or None if nothing matches
        """
        if self.only_existing and not (current_path / self._value).exists():
            return None

        stmt: Select = character_repository \
            .tag_values_by_name(character, *self.tag_names) \
            .where(Tag.value == self.target)

        with self.db.session() as session:
            result = session.scalar(stmt)

        if result:
            return self._value

        return None
