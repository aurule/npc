from typing import Iterator
from pathlib import Path

from functools import cached_property

from .pathfinder_class import Pathfinder
from npc.characters import Character, CharacterFactory, CharacterReader, CharacterWriter
from npc.db import DB, character_repository

class CharacterCollection():
    """Class for a group of Character objects, backed by a database

    Manages the loading, creation, and fetching of Characters
    """

    def __init__(self, campaign, *, db: DB = None):
        """Create a new CharacterCollection object

        Character files are not read immediately. Instead, call seed() to load
        all available records.
        """
        self.db = db if db else DB()

        self.campaign = campaign
        self.root = campaign.characters_dir
        self.count = 0
        self.item_type = "Character"

    def seed(self):
        new_characters = []
        factory = CharacterFactory(self.campaign)
        for character_path in self.valid_character_files():
            reader = CharacterReader(character_path)
            character = factory.make(
                realname = reader.name(),
                mnemonic = reader.mnemonic(),
                body = reader.body(),
                tags = reader.tags(),
                path = reader.character_path,
            )
            new_characters.append(character)
        with self.db.session() as session:
            session.execute(character_repository.destroy_all())
            session.add_all(new_characters)
            session.commit()
        self.count = len(new_characters)

    def refresh(self):
        """Reload changed npc files into the db

        This method checks all valid character files. Any that are new are loaded into the db. Any that have
        changed since they were loaded have their old records deleted and are added as new characters. Any
        records whose files no longer exist are deleted.
        """
        new_characters: list[Character] = []
        keep: list[int] = []
        valid_files: list[Path] = list(self.valid_character_files())
        factory = CharacterFactory(self.campaign)
        with self.db.session() as session:
            chars_query = character_repository.find_in(file_loc = [str(f) for f in valid_files])
            indexed_characters = {c.file_loc: c for (c,) in session.execute(chars_query).all()}
            for character_path in valid_files:
                record = indexed_characters.get(str(character_path))
                if record:
                    mtime = record.file_path.stat().st_mtime
                    if record.file_mtime >= mtime:
                        keep.append(record.id)
                        continue

                reader = CharacterReader(character_path)
                character = factory.make(
                    realname = reader.name(),
                    mnemonic = reader.mnemonic(),
                    body = reader.body(),
                    tags = reader.tags(),
                    path = reader.character_path,
                )
                new_characters.append(character)

            session.execute(character_repository.destroy_others(keep))
            session.add_all(new_characters)
            session.commit()

            self.count = len(new_characters) + len(keep)

    def valid_character_files(self) -> Iterator[Path]:
        """Iterate valid character file paths

        This iterator yields all paths within our root dir that match these criteria:
        * Has an allowed suffix
        * Not in an ignored subpath

        Returns:
            Iterator[Path]: Iterator of valid character files
        """
        ignore_paths = [self.root / p for p in self.campaign.settings.get("campaign.characters.ignore_subpaths")]
        def allowed(file_path):
            if file_path.suffix not in self.allowed_suffixes:
                return False

            for ignore_path in ignore_paths:
                if file_path.is_relative_to(ignore_path):
                    return False

            return True

        for character_path in self.root.glob("**/*"):
            if not allowed(character_path):
                continue

            yield character_path

    @cached_property
    def allowed_suffixes(self) -> set[str]:
        """Get the file suffixes that are allowed by this campaign

        The .npc suffix is always present. Suffixes used by each type's default sheet are also included.

        Returns:
            set[str]: Set of suffix strings
        """
        return {".npc"}.union({spec.default_sheet_suffix for spec in self.campaign.types.values()})

    def create(self, **kwargs) -> int:
        """Make and save a new character object

        The character object is created using the given kwargs and immediately persisted to the database. Our
        count of total characters is also updated.

        Returns:
            int: ID of the newly created character
        """
        factory = CharacterFactory(self.campaign)
        character = factory.make(**kwargs)

        with self.db.session() as session:
            session.add(character)
            session.commit()

        self.count += 1
        return character.id

    def all(self) -> list[Character]:
        """Get all character records

        These records will be detached from any session, so a different manual session will be needed to get
        their tags.

        Returns:
            list[Character]: List of the character objects
        """
        with self.db.session() as session:
            return session.scalars(character_repository.all())

    def get(self, id: int) -> Character:
        """Get a single character record by ID

        This record is detached from its session, so a different session will need to be used for further
        manipulation or getting tags.

        Args:
            id (int): ID of the character record

        Returns:
            Character: Character record associated with the given ID
        """
        with self.db.session() as session:
            return session.scalar(character_repository.get(id))

    def update(self, id: int, **kwargs):
        with self.db.session() as session:
            character = session.scalar(character_repository.get(id))
            for attr, value in kwargs.items():
                setattr(character, attr, value)
            session.commit()

    def apply_query(self, query):
        """Run an arbitrary query against this collection

        This is a convenience method to avoid working directly with the collection's db instance. Obviously,
        since this will happily execute any query, care should be taken to ensure the queries make sense for
        a character collection.

        Args:
            query (Query): Database query object

        Returns:
            Query: Database result from the query
        """
        with self.db.session() as session:
            return session.execute(query)
