from abc import ABC, abstractmethod
from pathlib import Path

from npc.db import DB
from npc.characters import Character

class BaseSubpathComponent(ABC):
    """Base subpath component class

    Defines the interface for subpath components. The only_existing flag is *optional* and only included
    because it can modify the database query in some components. Callers should enforce path existance
    themselves.

    Besides the explicit abstract elements, this base class' interface requires that the SELECTOR class
    attribute be defined. This is a unique name used to identify the subclass.

    Attributes:
        SELECTOR: The selector string
    """

    def __init__(self, db: DB, spec: dict, only_existing: bool):
        self.db: DB = db
        self.spec: dict = spec
        self.only_existing: bool = only_existing

    @abstractmethod
    def value(self, character: Character, current_path: Path) -> str:
        """The value of this component

        This might be a tag value, static string, some other piece of data, or None.

        Args:
            character (Character): The character to get values from
            current_path (Path): The constructed path so far

        Returns:
            str: Value of this subpath component
        """

    def from_spec(self, spec: dict, key: str):
        """Get a required value from the passed spec

        This gets the value of key from spec. If key isn't there, an error is raised.

        Args:
            spec (dict): Configuration data for the component
            key (str): Name of the key to fetch

        Returns:
            any: Value of the named key

        Raises:
            KeyError: Raised if the named key does not exist in spec
        """
        value = spec.get(key)
        if not value:
            raise KeyError(f"Missing {key} key for {self.__class__.SELECTOR} subpath component")
        return value
