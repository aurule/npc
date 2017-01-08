"""
Package for handling the NPC windowed interface
"""

import sys
from contextlib import contextmanager
from os import chdir, path, getcwd
from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import run

import npc
from npc import commands, settings

from .uis import *

def start(argv):
    """Main entry point for the GUI"""

    try:
        prefs = settings.Settings()
    except OSError as err:
        startup_error(err.strerror)

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

class MainWindow(Ui_MainWindow):
    def __init__(self, window, prefs):
        Ui_MainWindow.__init__(self)

        self.prefs = prefs
        self.campaign_root = path.expanduser('~')

        # main window setup
        self.window = window
        self.setupUi(window)
        self.force_titles()

        # about dialog
        self.about_dialog = QtWidgets.QDialog(self.window)
        AboutDialog(self.about_dialog)
        self.actionAbout.triggered.connect(self.about_dialog.open)

        # init dialog
        self.init_dialog = InitDialog(self.window)

        # commands setup
        self.actionOpenCampaign.triggered.connect(self.open_campaign)
        self.actionUserSettings.triggered.connect(self.run_user_settings)
        self.actionCampaignSettings.triggered.connect(self.run_campaign_settings)
        self.actionReloadSettings.triggered.connect(self.run_reload_settings)
        self.actionInit.triggered.connect(self.run_init)

        # quit menu entry
        self.actionQuit.triggered.connect(self.quit)

    def _show_error(self, title, message, parent=None):
        """
        Helper to show a modal error window

        Args:
            title (str): Title for the error window
            message (str): Message text to display
            parent (object): Parent window for the modal. This window will be
                disabled while the modal is visible. Defaults to the main window.
        """
        if not parent:
            parent = self.window
        errorbox = QtWidgets.QMessageBox.warning(parent, title, message, QtWidgets.QMessageBox.Ok)

    def force_titles(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))

    def open_campaign(self):
        campaign_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.window,
            'Open Campaign',
            self.campaign_root)
        if campaign_dir:
            self.set_campaign_root(campaign_dir)

    def set_campaign_root(self, root_dir):
        try:
            chdir(root_dir)
        except:
            self._show_error("Cannot open campaign", "Cannot open the folder at {}".format(root_dir))
            return
        self.campaign_root = root_dir
        self.run_reload_settings()

    @contextmanager
    def safe_command(self, command):
        try:
            yield command
        except AttributeError as err:
            self._show_error('Command failed', err)

    def run_user_settings(self):
        with self.safe_command(commands.open_settings) as command:
            result = command('user', show_defaults=True, prefs=self.prefs)

            if not result.success:
                self._show_error('Could not open user settings', result)
                return

            run([self.prefs.get("editor")] + result.openable)

    def run_campaign_settings(self):
        with self.safe_command(commands.open_settings) as command:
            result = command('campaign', show_defaults=True, prefs=self.prefs)

            if not result.success:
                self._show_error('Could not open campaign settings', result)
                return

            run([self.prefs.get("editor")] + result.openable)

    def run_reload_settings(self):
        try:
            new_prefs = settings.Settings()
        except OSError as err:
            self._show_error("Could not open settings", err.strerror)
            return

        changeling_errors = settings.lint_changeling_settings(new_prefs)
        if changeling_errors:
            message = "\n".join(changeling_errors)
            self._show_error("Error in changeling settings", message)
            return

        self.prefs = new_prefs
        self.window.setWindowTitle("NPC - {}".format(self.prefs.get('campaign')))

    def run_init(self):
        self.init_dialog.reset()
        if path.exists(self.prefs.get_settings_path('campaign')):
            self.init_dialog.set_campaign_name(self.prefs.get('campaign'), enabled=False)
        else:
            self.init_dialog.set_campaign_name(path.basename(getcwd()))

        if self.init_dialog.run():
            values = self.init_dialog.get_values()
            with self.safe_command(commands.init) as command:
                command(**values)

    def quit(self):
        QtCore.QCoreApplication.instance().quit()

class AboutDialog(Ui_AboutDialog):
    def __init__(self, dialog):
        Ui_AboutDialog.__init__(self)
        self.setupUi(dialog)
        self.labelVersion.setText("Version {0}".format(npc.VERSION))

class InitDialog(QtWidgets.QDialog, Ui_InitDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_InitDialog.__init__(self)

        self.setupUi(self)

    def reset(self):
        self.checkBoxCreateTypes.setChecked(False)
        self.initCampaignTitle.setText("")

    def set_campaign_name(self, new_name, enabled=True):
        self.initCampaignTitle.setText(new_name)
        self.initCampaignTitle.setEnabled(enabled)

    def get_values(self):
        return {
            "create_types": self.checkBoxCreateTypes.isChecked(),
            "campaign_name": self.initCampaignTitle.text()}

    def run(self):
        result = self.exec_()
        return result == self.Accepted
