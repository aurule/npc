from typing import Iterator, Callable
from pathlib import Path

from functools import cached_property

from .pathfinder_class import Pathfinder
from npc.characters import Character, CharacterFactory, CharacterReader, CharacterWriter
from npc.db import DB, character_repository
from npc.util.errors import NotFoundError

class CharacterCollection():
    """Class for a group of Character objects, backed by a database

    Manages the loading, creation, and fetching of Characters
    """

    CACHE_KEY = "characters"

    def __init__(self, campaign, *, db: DB = None):
        """Create a new CharacterCollection object

        Character files are not read immediately. Instead, call seed() to load
        all available records.
        """
        self.db = db if db else DB()

        self.campaign = campaign
        self.root = campaign.characters_dir
        self._count = 0
        self.item_type = "Character"

    @property
    def count(self) -> int:
        """Total number of characters in this collection

        This is here to prevent unnecessary sql count queries.

        Returns:
            int: Number of characters in the collection
        """
        return self._count

    @count.setter
    def count(self, value: int):
        """Set the number of characters in this collection

        This stores the new count locally as well as caches it in the campaign. Because of the file write for
        the cache, setting the character count is a relatively expensive operation that should be done as
        rarely as possible.

        Args:
            value (int): New value for the count of all characters
        """
        self._count = value
        self.campaign.stats.set(self.CACHE_KEY, value)

    def seed(self, progress_callback: Callable = None):
        """Load all npc filesinto the db

        This method is designed to be used when you want a clean load of all files. It clears out the
        characters table and loads every character file it can find, without any checking like refresh does.

        Args:
            progress_callback (Callable): Optional callback to update a progress bar
        """
        def default_progress():
            pass
        if progress_callback is None:
            progress_callback = default_progress

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
            progress_callback()
        with self.db.session() as session:
            session.execute(character_repository.destroy_all())
            session.add_all(new_characters)
            session.commit()
        self.count = len(new_characters)

    def refresh(self, progress_callback: Callable = None):
        """Reload changed npc files into the db

        This method checks all valid character files. Any that are new are loaded into the db. Any that have
        changed since they were loaded have their old records deleted and are added as new characters. Any
        records whose files no longer exist are deleted.

        Args:
            progress_callback (Callable): Optional callback to update a progress bar
        """
        def default_progress():
            pass
        if progress_callback is None:
            progress_callback = default_progress

        new_characters: list[Character] = []
        keep: list[int] = []
        valid_files: list[Path] = list(self.valid_character_files())
        factory = CharacterFactory(self.campaign)
        with self.db.session() as session:
            chars_query = character_repository.all()
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
                progress_callback()

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
        """Update a character record's attributes

        This method only allows updating the character's own attributes. Tags are entirely unsupported.

        Args:
            id (int): ID of the character record
            **kwargs: Attribute names and values to change on the character

        Raises:
            NotFoundError: When the ID does not have a character record
            AttributeError: When trying to set an attribute that does not exist on the record
        """
        with self.db.session() as session:
            character = session.scalar(character_repository.get(id))

            if not character:
                raise NotFoundError(f"No character exists with id {id}")
            for attr, value in kwargs.items():
                if not hasattr(character, attr):
                    raise AttributeError(name=attr, obj=character)
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
