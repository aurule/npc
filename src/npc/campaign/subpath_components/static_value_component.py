from pathlib import Path

from .base_component import BaseSubpathComponent
from npc.characters import Character
from npc.db import DB

class StaticValueComponent(BaseSubpathComponent):
    """Static Value subpath component

    This component always returns its static string.

    Attributes:
        SELECTOR: The selector string
    """

    SELECTOR = "static_value"

    def __init__(self, db: DB, spec: dict, only_existing: bool = False):
        super().__init__(db, spec, only_existing)

        self._value = spec.get("value")
        if not self._value:
            raise KeyError("Missing value key for static subpath component")

    def value(self, character: Character, current_path: Path) -> str:
        """Get our static value

        This is always the value from our configuration.

        Args:
            character (Character): Character object (ignored)
            current_path (Path): Path (ignored)

        Returns:
            str: Configured static string
        """
        return self._value
