class ValidationError():
    """Base validation error object

    Core interface for validation error messages.
    """

    def __init__(self, detail: str):
        self.detail = detail
        self.preamble = "Error"

    def __str__(self) -> str:
        """Printing the error object should result in a readable string

        Returns:
            str: The error message
        """
        return self.message

    @property
    def message(self) -> str:
        """Format a human-readable message for this error

        Puts the preamble before the detail message, separated by a colon.

        Returns:
            str: Readable error message
        """
        return f"{self.preamble}: {self.detail}"
