"""
Classes to represent error states
"""

"""Base exception class for NPC"""
class Error(Exception):
    pass

"""
Raised when trying to use a malformed file

Attributes:
    strerror (str): Error message describing what happened
"""
class FormatError(Error):
    def __init__(self, strerror):
        self.strerror = strerror

"""
Raised when a file parsing operation fails

Attributes:
    strerror (str): Error message describing what happened
    path (PathLike): Path to the offending file
    lineno (int): Line number of the failure, if known. Defaults to 0.
    colno (int): Column of the failure, if known. Defaults to 0.
"""
class ParseError(Error):
    def __init__(self, strerror: str, path, lineno: int = 0, colno: int = 0):
        self.strerror = strerror
        self.path = path
        self.lineno = lineno
        self.colno = colno
