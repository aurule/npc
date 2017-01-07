"""
Package for handling the NPC windowed interface
"""

import sys
from contextlib import contextmanager
from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import run

from .uis import *
from .. import commands, main, settings

def start():
    """Main entry point for the GUI"""

    try:
        prefs = settings.Settings()
    except OSError as err:
        startup_error(err.strerror)

    changeling_errors = settings.lint_changeling_settings(prefs)
    if changeling_errors:
        message = "\n".join(changeling_errors)
        startup_error(message)

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = MainWindow(window, prefs)

    window.show()
    sys.exit(app.exec_())

def startup_error(message):
    """
    Show an error that happened during startup

    This is used for errors that occur before the main UI has
    been created. Other errors should use _show_error.

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

def _show_error(parent, title, message):
    """
    Helper to show an modal error window

    Args:
        parent (object): Parent window for the modal. This
            window will be disabled while the modal is visible.
        title (str): Title for the error window
        message (str): Message text to display
    """
    errorbox = QtWidgets.QMessageBox.warning(parent, title, message, QtWidgets.QMessageBox.Ok)

class MainWindow(Ui_MainWindow):
    def __init__(self, window, prefs):
        self.prefs = prefs
        Ui_MainWindow.__init__(self)

        # main window setup
        self.window = window
        self.setupUi(window)
        self.force_titles()

        # about dialog
        self.about_dialog = QtWidgets.QDialog(window)
        about_dialog_content = AboutDialog(self.about_dialog)
        self.actionAbout.triggered.connect(self.about_dialog.open)

        # commands setup
        self.actionUserSettings.triggered.connect(self.run_user_settings)

        # quit menu entry
        self.actionQuit.triggered.connect(self.quit)

    def force_titles(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))

    @contextmanager
    def safe_command(self, command):
        try:
            yield command
        except AttributeError as err:
            _show_error(self.window, 'Command failed', err)

    def run_user_settings(self):
        with self.safe_command(commands.open_settings) as command:
            result = command('campaign', show_defaults=True)

            if not result.success:
                _show_error(self.window, 'Could not open user settings', result)

            run([self.prefs.get("editor")] + result.openable)

    def quit(self):
        QtCore.QCoreApplication.instance().quit()

class AboutDialog(Ui_AboutDialog):
    def __init__(self, dialog):
        Ui_AboutDialog.__init__(self)
        self.setupUi(dialog)
        self.labelVersion.setText("Version {0}".format(main.VERSION))
