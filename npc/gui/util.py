# Helpers common to the gui

from contextlib import contextmanager
from PyQt5 import QtWidgets

@contextmanager
def safe_command(command):
    """
    Helper to suppress AttributeErrors from commands

    Args:
        command (callable): The command to run. Any AttributeError raised by
            the command will be suppressed.
    """
    try:
        yield command
    except AttributeError as err:
        pass

def show_error(title, message, parent):
    """
    Helper to show a modal error window

    Args:
        title (str): Title for the error window
        message (str): Message text to display
        parent (object): Parent window for the modal. This window will be
            disabled while the modal is visible. Defaults to the main window.
    """
    QtWidgets.QMessageBox.warning(parent, title, message, QtWidgets.QMessageBox.Ok)
