from abc import ABC, abstractmethod

class Taggable(ABC):
    """Abstract class for objects which can store tags

    The Character and Tag classes can both store tags, but use different internal implementations.
    """

    @abstractmethod
    def accepts_tag(self, tag_name: str) -> bool:
        """Whether this object allows the named tag in its tags collection

        Args:
            tag_name (str): Name of the tag to test

        Returns:
            bool: True if the object accepts the named tag, False if not
        """
        pass

    @abstractmethod
    def add_tag(self, tag):
        """Add the given Tag to the object

        Args:
            tag (Tag): Tag to add
        """
        pass
