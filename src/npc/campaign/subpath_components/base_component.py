from abc import ABC, abstractmethod
from pathlib import Path

from npc.db import DB
from npc.characters import Character

class BaseSubpathComponent(ABC):
    """Base subpath component class

    Defines the interface for subpath components. The only_existing flag is *optional* and only included
    because it can modify the database query in some components, or be used as an optimization in others.
    Callers should enforce path existance themselves.

    Besides the explicit abstract elements, this base class' interface requires that the SELECTOR class
    attribute be defined. This is a unique name used to identify the subclass.

    The only spec key universally allowed is the special `fallback` key, whose value is returned if the main
    value method returns something falsy.

    Attributes:
        SELECTOR: The selector string
    """

    def __init__(self, db: DB, spec: dict, only_existing: bool):
        self.db: DB = db
        self.spec: dict = spec
        self.only_existing: bool = only_existing
        self.fallback: str

        try:
            self.fallback = self.from_spec("fallback")
        except KeyError:
            self.fallback = None

    @abstractmethod
    def tag_value(self, character: Character, current_path: Path) -> str:
        """The tag-derived value of this component

        This might be a tag value, static string, some other piece of data, or None. It is usually based in
        some way on the character's tags, but not always. If this returns None, the fallback value will be
        returned by the caller if it's set.

        Args:
            character (Character): The character to examine
            current_path (Path): The constructed path so far

        Returns:
            str: Value of this subpath component
        """

    def value(self, character: Character, current_path: Path) -> str:
        """The final value of this component

        This method tries to return the result of tag_value first. If that is falsy, then the value of our
        fallback is returned instead.

        Args:
            character (Character): The character to examine
            current_path (Path): The constructed path so far

        Returns:
            str: Final value of this subpath component
        """
        return self.tag_value(character, current_path) or self.fallback

    def from_spec(self, key: str):
        """Get a required value from the passed spec

        This gets the value of key from our spec. If key isn't there, an error is raised.

        Args:
            key (str): Name of the key to fetch

        Returns:
            any: Value of the named key

        Raises:
            KeyError: Raised if the named key does not exist in spec
        """
        value = self.spec.get(key)
        if not value:
            raise KeyError(f"Missing {key} key for {self.__class__.SELECTOR} subpath component")
        return value
