from pathlib import Path

from .relocation_class import Relocation

class BaseReorganizer:
    """Class for handling file reorganization

    Specific subclasses are meant to implement their own gather_paths methods. This class handles all of the
    core logic of conflict resolution and warnings.
    """

    def __init__(self):
        self.relocations: list[Relocation] = []

    def gather_paths(self):
        """Method to gather the ideal paths for a certain type of record

        Subclasses should use this method to populate relocations with Relocation instances.

        This is not implemented by default, although the base reorganizer can be used by manually populating
        the relocations list.

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
        for recpath in self.relocations:
            if recpath.ideal_path in unique_paths:
                conflicting_paths.add(recpath.ideal_path)
            else:
                unique_paths.add(recpath.ideal_path)

        return [f"Multiple files want to use the path '{cpath}'" for cpath in conflicting_paths]

    def make_movement_plan(self) -> list[Relocation]:
        """Create an ordered list of files moves to reach all of the ideal paths

        This method removes any Relocation which are already satisfied. Then it makes sure that any
        Relocation whose current path is another record's ideal path are moved out of the way first.

        Returns:
            list[Relocation]: List of Relocation objects which can safely be executed
        """
        plan: list[Relocation] = [r for r in self.relocations if not r.satisfied]

        return sorted(plan)

    def execute_movement_plan(self, plan: list[Relocation]):
        pass
        # execute the movement plan in order
