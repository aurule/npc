"""
Classes for returning data
"""

class Result:
    """
    Data about the result of a subcommand

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
