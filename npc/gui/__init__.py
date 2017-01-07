"""
Package for handling the NPC windowed interface
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import run

from .uis import *
from .. import commands, main, settings

class MainWindow(Ui_MainWindow):
    def __init__(self, window):
        self.prefs = settings.InternalSettings()
        Ui_MainWindow.__init__(self)

        self.setupUi(window)
        self.force_titles()

        self.about_dialog = QtWidgets.QDialog()
        about_dialog_content = About(self.about_dialog)
        self.actionAbout.triggered.connect(self.about_dialog.open)

        self.actionUserSettings.triggered.connect(self.run_user_settings)

        self.actionQuit.triggered.connect(self.quit)

    def quit(self):
        QtCore.QCoreApplication.instance().quit()

    def force_titles(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))

    def run_user_settings(self):
        try:
            result = commands.open_settings('campaign', show_defaults=True)
        except AttributeError as err:
            messagebox.showerror("Error!", err)

        if not result.success:
            messagebox.showerror("Error!", result)

        if result.openable:
            run([self.prefs.get("editor")] + result.openable)

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
