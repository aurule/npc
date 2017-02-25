"""
Package for handling the NPC windowed interface
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import npc
from npc import settings

from .main_window import MainWindow

def start(argv=None):
    """Main entry point for the GUI"""

    try:
        prefs = settings.Settings()
    except OSError as err:
        startup_error(err.strerror)

    if not argv:
        argv = sys.argv[1:]

    changeling_errors = settings.lint_changeling_settings(prefs)
    if changeling_errors:
        message = "\n".join(changeling_errors)
        startup_error(message)

    app = QtWidgets.QApplication(argv)
    window = QtWidgets.QMainWindow()

    prog = MainWindow(window, prefs)

    window.show()
    sys.exit(app.exec_())

def startup_error(message):
    """
    Show an error that happened during startup

    This is used for errors that occur before the main UI has
    been created.

    Args:
        message (str): Message text to display
    """
    app = QtWidgets.QApplication([])
    errorbox = QtWidgets.QMessageBox.critical(
        None,
        'Could not start NPC',
        message,
        QtWidgets.QMessageBox.Ok)
    sys.exit()

def _translate(*args, **kwargs):
    QtCore.QCoreApplication.translate(*args, **kwargs)
