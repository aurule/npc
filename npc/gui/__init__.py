"""
Package for handling the NPC windowed interface
"""

import argparse
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import npc
from npc import settings

from .main_window import MainWindow

def start(argv=None):
    """Main entry point for the GUI"""

    parser = _make_parser()
    if not argv:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)

    try:
        prefs = settings.Settings()
    except OSError as err:
        startup_error(err.strerror)

    setting_errors = settings.lint_settings(prefs)
    if setting_errors:
        message = "Error in settings\n".join(setting_errors)
        startup_error(message)

    app = QtWidgets.QApplication(argv)
    window = QtWidgets.QMainWindow()

    prog = MainWindow(window, prefs, campaign=args.campaign)

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
    QtWidgets.QMessageBox.critical(
        None,
        'Could not start NPC',
        message,
        QtWidgets.QMessageBox.Ok)
    sys.exit()

def _translate(*args, **kwargs):
    QtCore.QCoreApplication.translate(*args, **kwargs)

def _make_parser():
    """
    Construct the arguments parser

    Returns:
        Complete argparser object
    """

    parser = argparse.ArgumentParser(description='GM helper script to manage game files - GUI')
    parser.add_argument('--campaign', default=None, help="Use the campaign files in a different directory", metavar='DIR')
    parser.add_argument('--version', action='version', version=npc.__version__)
    parser.set_defaults(debug=False)

    return parser

