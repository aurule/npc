from sqlalchemy import Select
from pathlib import Path

from .base_component import BaseSubpathComponent
from npc.characters import Character
from npc.db import DB, character_repository

class ConditionalValueComponent(BaseSubpathComponent):
    """Conditional Value subpath component

    This component returns a static string if the character has at least one of the listed tags.

    Attributes:
        SELECTOR: The selector string
    """

    SELECTOR = "conditional_value"

    def __init__(self, db: DB, spec: dict, only_existing: bool = False):
        super().__init__(db, spec, only_existing)

        self.tag_names: list[str] = spec.get("tags")
        if not self.tag_names:
            raise KeyError("Missing tags key for conditional value subpath component")

        self._value = spec.get("value")
        if not self._value:
            raise KeyError("Missing value key for conditional value subpath component")

    def value(self, character: Character, current_path: Path) -> str:
        """Return the configured static value if character has at least one of our tags

        Args:
            character (Character): Character to test
            current_path (Path): Current working path (ignored)

        Returns:
            str: The configured value, if character has at least one of our tags. Otherwise, None.
        """
        if self.only_existing and not (current_path / self._value).exists():
            return None

        stmt: Select = character_repository.has_tags(character, *self.tag_names)

        with self.db.session() as session:
            result = session.scalar(stmt)

        if result:
            return self._value

        return None
