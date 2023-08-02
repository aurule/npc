from dataclasses import dataclass
from pathlib import Path

@dataclass
class RecordPaths:
    """Container for path information

    Attributes:
        id: ID of the record
        current_path: Its current path
        ideal_path: Its ideal path
    """

    id: int
    current_path: Path
    ideal_path: Path

class BaseReorganizer:
    """Class for handling file reorganization

    Specific subclasses are meant to implement their own gather_paths methods. This class handles all of the
    core logic of conflict resolution and warnings.
    """

    def __init__(self):
        self.record_paths: list[RecordPaths] = []

    def gather_paths(self):
        """Method to gather the ideal paths for a certain type of record

        Subclasses should use this method to populate record_paths with RecordPaths instances.

        This is not implemented by default, although the base reorganizer can be used by manually populating
        the record_paths list.

        Raises:
            NotImplementedError: Subclasses should implement this method to get the current and ideal paths
            for the records they operate on.
        """
        raise NotImplementedError

    def check_conflicts(self) -> list[str]:
        """Check for problems with the generated ideal paths

        This checks for problems in the ideal paths that cannot be resolved automatically. Currently, just one
        check is performed:

        1. Every ideal path must be unique

        Returns:
            list[str]: List of error messages. If it's empty, all is well.
        """
        messages: list[str] = []
        conflicting_paths: set[Path] = set()

        unique_paths: set[Path] = set()
        for recpath in self.record_paths:
            if recpath.ideal_path in unique_paths:
                conflicting_paths.add(recpath.ideal_path)
            else:
                unique_paths.add(recpath.ideal_path)

        return [f"Multiple files want to use the path '{cpath}'" for cpath in conflicting_paths]

    def make_movement_plan(self) -> list[RecordPaths]:
        pass
        # skip all entries where a current path matches its ideal path
        # if a current path is an ideal path, move it first

    def execute_movement_plan(self, plan: list[RecordPaths]):
        pass
        # execute the movement plan in order
