import re
from pathlib import Path

class PlanningFilename:
    """Represents a single filename pattern

    Allows for mutations and pattern expansion to be done in one place
    """

    index_regex = r'\(\((?P<width>N+)\)\)'

    def __init__(self, filename_pattern: str):
        self.filename_pattern = filename_pattern

    @property
    def basename(self) -> str:
        """Get the non-extension portion of the filename

        Given "session.md", this returns "session".

        Returns:
            str: Filename without its extension suffix
        """
        return Path(self.filename_pattern).stem

    @property
    def index_capture_regex(self) -> str:
        """Create a regex that matches our filename and captures its index number

        Replaces the ((N)) placeholder with a regex capture group so that the index of a real filename can be
        found.

        Returns:
            str: Regex with a "number" capture group
        """
        # The lambda is **required**, or re.sub() balks at the \d in our replacement string
        return re.sub(self.index_regex, lambda m: '(?P<number>\\d+)', self.basename)

    @property
    def index_width(self) -> int:
        """Get the number of N characters in the index placeholder

        This lets the total number of Ns define padding for the index. For example, the placeholder ((N))
        returns 1, while ((NNN)) returns 3.

        Returns:
            int: Number of Ns in the placeholder
        """
        match = re.search(self.index_regex, self.filename_pattern)
        if not match:
            return 0
        return len(match.group("width"))

    def for_index(self, index: int) -> str:
        """Generate the filename for a given index

        Replace the index placeholder with the given index number. If the number has fewer digits than the
        pattern's index width, pad it with leading zeros.

        Args:
            index (int): Index number to insert

        Returns:
            str: Filename with the index number inserted
        """
        return re.sub(self.index_regex, str(index).rjust(self.index_width, "0"), self.filename_pattern)
