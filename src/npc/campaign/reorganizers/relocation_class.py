from dataclasses import dataclass
from pathlib import Path

@dataclass
class Relocation:
    """Container for path information

    Attributes:
        id: ID of the record
        current_path: Its current path
        ideal_path: Its ideal path
    """

    id: int
    current_path: Path
    ideal_path: Path

    def __lt__(self, other) -> bool:
        return self.current_path == other.ideal_path

    @property
    def satisfied(self) -> bool:
        return self.current_path == self.ideal_path
