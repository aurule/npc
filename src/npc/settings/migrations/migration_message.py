from pathlib import Path

class MigrationMessage:
    """Simple message class for communicating what changes were made

    This class is designed to be used programmatically to construct message strings.
    """
    def __init__(self, message: str, file: Path = None, key: str = None):
        self.message = message
        self.file = file
        self.key = key

    def __repr__(self):
        return f"MigrationMessage(message={self.message!r}, file={self.file!r}, key={self.key!r})"
