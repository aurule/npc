"""
Classes to represent error states
"""

class Error(Exception):
    """Base exception class for NPC"""
    pass

class FormatError(Error):
    """
    Raised when trying to use a malformed file

    Attributes:
        strerror (str): Error message describing what happened
    """
    def __init__(self, strerror):
        self.strerror = strerror

class ParseError(Error):
    """
    Raised when a parsing operation fails

    Attributes:
        strerror (str): Error message describing what happened
        path (PathLike): Path to the offending file
        lineno (int): Line number of the failure, if known. Defaults to 0.
        colno (int): Column of the failure, if known. Defaults to 0.
    """
    def __init__(self, strerror, path, lineno=0, colno=0):
        self.strerror = strerror
        self.path = path
        self.lineno = lineno
        self.colno = colno
