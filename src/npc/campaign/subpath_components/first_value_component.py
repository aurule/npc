from sqlalchemy import Select
from pathlib import Path

from .base_component import BaseSubpathComponent
from npc.characters import Character, Tag
from npc.db import DB, character_repository

class FirstValueComponent(BaseSubpathComponent):
    """First Value subpath component

    This component uses the first value found within the specified tags. When only_existing is true, the tags
    are first filtered by whether their value matches an existing directory.

    Attributes:
        SELECTOR: The selector string
    """

    SELECTOR = "first_value"

    def __init__(self, db: DB, spec: dict, only_existing: bool = False):
        super().__init__(db, spec, only_existing)

        self.tag_names = self.from_spec("tags")

    def value(self, character: Character, current_path: Path) -> str:
        """Get the value of this component

        This tries to return the first value of the first tag in our tag_names which the character has. When
        only_existing is true, it returns the first value of the first tag which the character has that
        already exists as a directory under current_path.

        Args:
            character (Character): The character to get tags for
            current_path (Path): The path to check for existing directories

        Returns:
            str: A new directory name, or None if nothing matches
        """
        stmt: Select = character_repository.tag_values_by_name(character, *self.tag_names)

        if self.only_existing:
            existing_dirs: list = [child.name for child in current_path.iterdir() if child.is_dir()]
            stmt = stmt.where(Tag.value.in_(existing_dirs))

        with self.db.session() as session:
            result_value = session.execute(stmt).scalar()

        return result_value
