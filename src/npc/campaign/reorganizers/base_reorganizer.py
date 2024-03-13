from pathlib import Path
from shutil import move

from .relocation_class import Relocation

class BaseReorganizer:
    """Class for handling file reorganization

    Specific subclasses are meant to implement their own gather_paths methods. This class handles all of the
    core logic of conflict resolution and warnings.
    """

    def __init__(self):
        self.relocations: list[Relocation] = []

    def add_relocation(self, id: int, current_path: Path, ideal_path: Path):
        """Simple helper method to add a relocation to our list

        Intended to make subclasses easier to use.

        Args:
            id (int): ID of the record to move
            current_path (Path): Current path of the record's file
            ideal_path (Path): Target path of the record's file
        """
        self.relocations.append(Relocation(id, current_path, ideal_path))

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
        for reloc in self.relocations:
            if reloc.ideal_path in unique_paths:
                conflicting_paths.add(reloc.ideal_path)
            else:
                unique_paths.add(reloc.ideal_path)

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

    def execute_movement_plan(self, plan: list[Relocation], progress_callback = None):
        """Move files in order as given in the list

        Each relocation object is executed, causing the file at its current_path to be moved to the
        ideal_path. If the ideal_path's parents do not exist, they are created first.

        This method can theoretically throw all kinds of filesystem errors if something goes wrong. See
        the documentation for shutil.move for details.

        Args:
            plan (list[Relocation]): List of relocation objects that describe file moves
            progress_callback (Callable): Optional callback to update a progress bar
        """
        def default_progress():
            pass
        if progress_callback is None:
            progress_callback = default_progress

        for reloc in plan:
            if not reloc.ideal_path.parent.exists():
                reloc.ideal_path.parent.mkdir(parents=True, exist_ok=True)

            move(reloc.current_path, reloc.ideal_path)
            self.after_move(reloc)
            progress_callback()

    def after_move(self, relocation: Relocation):
        """Optional hook for performing some action after a file has been moved

        This is intended for quick operations like updating a database field with the new path.

        Args:
            relocation (Relocation): The relocation that was just executed.
        """
        return
