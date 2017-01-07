"""
Package for handling the NPC windowed interface
"""

import sys
from contextlib import contextmanager
from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import run

from .uis import *
from .. import commands, main, settings

class MainWindow(Ui_MainWindow):
    def __init__(self, window):
        self.prefs = settings.InternalSettings()
        Ui_MainWindow.__init__(self)

        # main window setup
        self.setupUi(window)
        self.force_titles()

        # about dialog
        self.about_dialog = QtWidgets.QDialog(window)
        about_dialog_content = About(self.about_dialog)
        self.actionAbout.triggered.connect(self.about_dialog.open)

        # commands setup
        self.actionUserSettings.triggered.connect(self.run_user_settings)

        # quit menu entry
        self.actionQuit.triggered.connect(self.quit)

    def force_titles(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))

    def run_user_settings(self):
        with safe_command(commands.open_settings) as command:
            result = command('campaign', show_defaults=True)

            if not result.success:
                messagebox.showerror("Error!", result)

            run([self.prefs.get("editor")] + result.openable)

    def quit(self):
        QtCore.QCoreApplication.instance().quit()

@contextmanager
def safe_command(command):
    try:
        yield command
    except AttributeError as err:
        messagebox.showerror("Error!", err)

class About(Ui_AboutDialog):
    def __init__(self, dialog):
        Ui_AboutDialog.__init__(self)
        self.setupUi(dialog)
        self.labelVersion.setText("Version {0}".format(main.VERSION))

def start():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = MainWindow(window)

    window.show()
    sys.exit(app.exec_())
