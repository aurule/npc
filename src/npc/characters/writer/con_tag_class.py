from dataclasses import dataclass, field

@dataclass
class ConTag:
    """Object representing emittable tag-like data

    This class is for emitting tags which do not exist as individual Tag
    records: realname, character flags, etc.

    Attributes:
        name: Name of the tag
        value: Value of the tag (optional)
    """
    name: str
    value: str = None
    id: int = None
    subtags: list = field(default_factory=list)

    def emit(self) -> str:
        """Generate a parseable representation of this tag

        The value is only included if set and non-falsey.
            @flag
            @tag value

        Returns:
            str: Parseable version of the tag
        """
        out = f"@{self.name}"
        if self.value:
            out += (f" {self.value}")

        return out

    def __hash__(self) -> int:
        """Get a hash for this contag

        Generates a hash based on the contag name and value attributes

        Returns:
            int: Hash of this contag's name and value
        """
        return hash((self.name, self.value))

    def __eq__(self, other) -> bool:
        """Test whether this contag is the same as another contag

        Args:
            other (ConTag): ConTag to test against

        Returns:
            bool: True if both contags' hashes match, False if not
        """
        if not isinstance(other, ConTag):
            return NotImplemented

        return hash(self) == hash(other)
