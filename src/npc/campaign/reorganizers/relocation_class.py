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
        """Compare against another relocation

        This method is made to be used for sorting lists. A Relocation is considered less than another when
        its current path matches the other's ideal path. This sorts Relocations such that when applied in
        order, conflicting files will be moved out of the way before their path is taken.

        Args:
            other (Relocation): The other relocation to compare against

        Returns:
            bool: True if our current path matches other's ideal path, False if not

        Raises:
            NotImplementedError: Relocations cannot be compared against any other type
        """
        if not isinstance(other, self.__class__):
            raise NotImplementedError

        return self.current_path == other.ideal_path

    @property
    def satisfied(self) -> bool:
        """Get whether this relocation has been done

        A relocation with matching current and ideal paths does not need to be used, as the file is already at
        its ideal location.

        Returns:
            bool: True if current path matches ideal path, false if not
        """
        return self.current_path == self.ideal_path
