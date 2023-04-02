"""
Classes to represent error states
"""

class Error(Exception):
    """Base exception class for NPC"""
    pass

class ParseError(Error):
    """
    Raised when a file parsing operation fails

    Attributes:
        strerror (str): Error message describing what happened
        path (PathLike): Path to the offending file
        lineno (int): Line number of the failure, if known. Defaults to 0.
        colno (int): Column of the failure, if known. Defaults to 0.
    """
    def __init__(self, strerror: str, path, lineno: int = 0, colno: int = 0):
        self.strerror = strerror
        self.path = path
        self.lineno = lineno
        self.colno = colno

class SchemaError(Error):
    """Raised when there is a conflict between expected setting value types

    Args:
        strerror (str): Error message describing what happened
        path (PathLike): Path to the offending file. Usually None
        lineno (int): Line number of the failure, if known. Defaults to 0.
        colno (int): Column of the failure, if known. Defaults to 0.
    """
    def __init__(self, strerror: str, path = None, lineno: int = 0, colno: int = 0):
        self.strerror = strerror
