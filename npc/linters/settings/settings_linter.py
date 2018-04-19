"""Base settings linter class"""

from contextlib import contextmanager

class SettingsLinter:
    """Generic linter superclass"""
    def __init__(self, prefs):
        self.prefs = prefs
        self.errors = []
        self.error_prefix = '*'

    def lint(self):
        """
        Lint the given prefs

        Args:
            prefs (Settings): Settings object to lint

        Returns:
            A list of strings representing errors.
        """
        raise NotImplementedError

    @property
    def valid(self):
        return not self.errors

    def add_error(self, message):
        """
        Add an error to the log

        Adds the message to the internal errors, prefixed with self.error_prefix

        Args:
            message (string): Error text to add
        """
        self.errors.append("{} {}".format(self.error_prefix, message))

    def add_errors(self, messages):
        """
        Add multiple errors to the log

        Adds every element of messages to the internal errors log

        Args:
            messages (list[string]): List of strings to add as errors
        """
        for message in messages:
            self.add_error(message)

    @contextmanager
    def error_section(self, message):
        """
        Add a section to the error log

        This section starts with a header message, then indents all further
        error messages so they visually lie within that section.

        Args:
            message (string): Section header

        Yields:
            Cedes control as a context manager after setting an appropriate
            error prefix.
        """
        self.add_error(message)
        self.error_prefix = '  -'
        yield
        self.error_prefix = '*'
