from abc import ABC, abstractmethod

from npc.settings.tags import TagSpec

class TagDefiner(ABC):
    """Abstract class for objects which can define tag specs"""

    @abstractmethod
    def tags(self) -> dict:
        """Get the tags configured for this definer

        Combines tag definitions from one or more sources

        Returns:
            dict: Dict of TagSpec objects indexed by tag key
        """

    @abstractmethod
    def get_tag(self, tag_name: str) -> TagSpec:
        """Get a single tag as configured for this definer

        Uses combined tag definitions from one or more sources

        Args:
            tag_name (str): Name of the tag to get

        Returns:
            TagSpec: Spec of the named tag, or a new UndefinedTagSpec if that tag has no definition
        """
