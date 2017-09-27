"""
Classes for returning data
"""

class Result:
    """
    Data about the result of a subcommand

    A more specific result class should be used whenever possible

    Attributes:
        success (bool): Whether the subcommand ran correctly
        openable (list): Paths to files which were changed by or are relevant to
            the subcommand
        errcode (int): Error code indicating the type of error encountered.

            Error codes:
            0 -- Everything's fine
            1 -- Tried to create a file that already exists
            2 -- Latest plot and session files have different numbers
            3 -- Feature is not yet implemented
            4 -- Filesystem error
            5 -- Unrecognized format
            6 -- Invalid option
            7 -- Unrecognized template
            8 -- Missing required file
        errmsg (str): Human-readable error message. Will be displayed to the
            user.
        printables (list[str]): List of strings that detail changes made. Safe to
            leave blank.
    """
    def __init__(self, success, **kwargs):
        super().__init__()
        self.success = success
        self.openable = kwargs.get('openable', [])
        self.errcode = kwargs.get('errcode', 0)
        self.errmsg = kwargs.get('errmsg', '')
        self.printables = kwargs.get('printables', [])

    def __str__(self):
        if self.success:
            return "Success"
        return self.errmsg

    def __bool__(self):
        return self.success

class Success(Result):
    """Data about the successful result of a command"""
    def __init__(self, **kwargs):
        super().__init__(True, errcode=0, **kwargs)

    def __str__(self):
        return "Success"

    def __bool__(self):
        return True

class Failure(Result):
    """
    Data about a generic failure result

    A more specific error class should be used whenever possible
    """
    def __init__(self, **kwargs):
        super().__init__(False, **kwargs)

    def __str__(self):
        return self.errmsg

    def __bool__(self):
        return False

class FSError(Failure):
    """Data about a failure due to external filesystem problems"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class OptionError(Failure):
    """Data about a failure due to unrecognized options"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
