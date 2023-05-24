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
