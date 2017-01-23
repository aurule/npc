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
    """
    Show and run the GUI

    This class handles all the management of the campaign, including showing
    dialogs and running commands.
    """
    def __init__(self, window, prefs):
        Ui_MainWindow.__init__(self)

        self.prefs = prefs
        self.campaign_root = path.expanduser('~')

        # main window setup
        self.window = window
        self.setupUi(window)
        self.force_titles()

        self.recentCampaignActions = [QtWidgets.QAction(self.menuOpen_Recent_Campaign, visible=False, triggered=self.open_recent_campaign) for i in range(5)]
        for act in self.recentCampaignActions:
            self.menuOpen_Recent_Campaign.addAction(act)
        self._update_recent_campaigns()

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
        self.actionNew_Character.triggered.connect(self.run_new_character)

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

    def _update_recent_campaigns(self):
        """
        Update the recent campaigns list

        Loads recent campaign info from QSettings and creates menu items for
        each. If there are none, the menu is disabled.
        """
        settings = QtCore.QSettings('Aurule', 'NPC')
        campaign_paths = settings.value('recentCampaigns/paths', [])
        campaign_titles = settings.value('recentCampaigns/titles', [])

        num_recent_campaigns = min(len(campaign_paths), 5)

        for i in range(num_recent_campaigns):
            text = "&{num}. {title} ({path})".format(
                                        num=i+1,
                                        title=campaign_titles[i],
                                        path=campaign_paths[i])
            self.recentCampaignActions[i].setText(text)
            self.recentCampaignActions[i].setData(campaign_paths[i])
            self.recentCampaignActions[i].setVisible(True)

        for action in self.recentCampaignActions[num_recent_campaigns:]:
            action.setVisible(False)

        self.menuOpen_Recent_Campaign.setEnabled(num_recent_campaigns > 0)

    def force_titles(self):
        """
        Set real titles for File and Settings menus

        The text for these menus is generated by Qt5Designer and I can't get it
        to use anything other than its default string. This workaround makes
        them use sane mnemonics.
        """
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))

    def open_campaign(self):
        """
        Loads a campaign directory from the file picker

        See set_campaign_root for the heavy lifting.
        """
        campaign_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.window,
            'Open Campaign',
            self.campaign_root)
        if campaign_dir:
            self.set_campaign_root(campaign_dir)

    def open_recent_campaign(self):
        """
        Loads a campaign directory from the recent campaigns menu

        See set_campaign_root for the heavy lifting.
        """
        action = self.window.sender()
        if action:
            self.set_campaign_root(action.data())

    def set_campaign_root(self, root_dir):
        """
        Load a given campaign directory

        This handles all the work of actually loading a campaign.
        """
        try:
            chdir(root_dir)
        except:
            self._show_error("Cannot open campaign", "Cannot open the folder at {}".format(root_dir))
            return
        self.campaign_root = root_dir
        self.run_reload_settings()

        settings = QtCore.QSettings('Aurule', 'NPC')
        campaigns = settings.value('recentCampaigns/paths', [])
        campaign_titles = settings.value('recentCampaigns/titles', [])

        try:
            campaigns.remove(root_dir)
            campaign_titles.remove(root_dir)
        except ValueError:
            pass

        campaigns.insert(0, root_dir)
        campaign_titles.insert(0, self.prefs.get('campaign'))
        del campaigns[5:]
        del campaign_titles[5:]

        settings.setValue('recentCampaigns/paths', campaigns)
        settings.setValue('recentCampaigns/titles', campaign_titles)
        self._update_recent_campaigns()

    @contextmanager
    def safe_command(self, command):
        """
        Helper to prevent useless AttributeErrors from commands

        Args:
            command (callable): The command to run. Any AttributeError raised by
            the command will be suppressed.

        Yields:
            The command passed
        """
        try:
            yield command
        except AttributeError as err:
            self._show_error('Command failed', err)

    @contextmanager
    def dialog(self, dialog_class, *args, **kwargs):
        """
        Create and clean up after a dialog window class

        When leaving the context, the dialog is deleted to
        prevent memory problems in QT.

        Args:
            dialog_class (Class): The dialog class to create
            *args, **kwargs: Passed directly to the constructor

        Yields:
            An instance created from dialog_class
        """
        dlg = dialog_class(*args, **kwargs)
        try:
            yield dlg
        finally:
            dlg.deleteLater()

    def run_user_settings(self):
        """Run the user settings command"""
        with self.safe_command(commands.open_settings) as command:
            result = command('user', show_defaults=True, prefs=self.prefs)

            if not result.success:
                self._show_error('Could not open user settings', result.errmsg)
                return

            run([self.prefs.get("editor")] + result.openable)

    def run_campaign_settings(self):
        """Run the campaign settings command"""
        with self.safe_command(commands.open_settings) as command:
            result = command('campaign', show_defaults=True, prefs=self.prefs)

            if not result.success:
                self._show_error('Could not open campaign settings', result.errmsg)
                return

            run([self.prefs.get("editor")] + result.openable)

    def run_reload_settings(self):
        """Reparse and lint the settings"""
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
        """Run the init command with inputs from its dialog"""
        self.init_dialog.reset()
        if path.exists(self.prefs.get_settings_path('campaign')):
            self.init_dialog.set_campaign_name(self.prefs.get('campaign'), enabled=False)
        else:
            self.init_dialog.set_campaign_name(path.basename(getcwd()))

        if self.init_dialog.run():
            values = self.init_dialog.get_values()
            with self.safe_command(commands.init) as command:
                command(**values)

    def run_new_character(self):
        with self.dialog(NewCharacterDialog, self.window, self.prefs) as new_character_dialog:
            if not new_character_dialog.run():
                return

            values = new_character_dialog.values
            cmd = values.pop("command")
            with self.safe_command(cmd) as command:
                serial_args = [values.pop(k) for k in values.get('serialize', [])]

                result = command(*serial_args, **values)
                if not result.success:
                    self._show_error("Could not create character", result.errmsg)
                    return
            new_character_dialog.deleteLater()

    def quit(self):
        QtCore.QCoreApplication.instance().quit()

class AboutDialog(Ui_AboutDialog):
    """Create the About dialog"""
    def __init__(self, dialog):
        Ui_AboutDialog.__init__(self)
        self.setupUi(dialog)
        self.labelVersion.setText("Version {0}".format(npc.VERSION))

class InitDialog(QtWidgets.QDialog, Ui_InitDialog):
    """Show inputs for the campaign init dialog"""
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_InitDialog.__init__(self)

        self.setupUi(self)

        self.checkBoxCreateTypes.stateChanged.connect(self.update_dirlist)

    @contextmanager
    def safe_command(self, command):
        """
        Helper to prevent useless AttributeErrors from commands

        Args:
            command (callable): The command to run. Any AttributeError raised by
            the command will be suppressed.
        """
        try:
            yield command
        except AttributeError as err:
            pass

    def update_dirlist(self):
        """Update the preview of directories to create"""
        values = self.get_values()
        with self.safe_command(commands.init) as command:
            result = command(dryrun=True, **values)
            self.initFoldersToCreate.setText("\n".join(sorted(result.changes)))

    def reset(self):
        """Reset the dialog inputs to their default state"""
        self.checkBoxCreateTypes.setChecked(False)
        self.initCampaignTitle.setText("")

    def set_campaign_name(self, new_name, enabled=True):
        """
        Set the default campaign name and whether it can be edited

        Args:

        """
        self.initCampaignTitle.setText(new_name)
        self.initCampaignTitle.setEnabled(enabled)

    def get_values(self):
        """Get structured data from the inputs"""
        return {
            "create_types": self.checkBoxCreateTypes.isChecked(),
            "campaign_name": self.initCampaignTitle.text()}

    def run(self):
        """
        Show the dialog

        Returns:
            True if the OK button was pressed, False if not. Use the get_values
            method to retrieve the user's inputs.
        """

        result = self.exec_()
        return result == self.Accepted

class NewCharacterDialog(QtWidgets.QDialog, Ui_NewCharacterDialog):
    def __init__(self, parent, prefs):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_NewCharacterDialog.__init__(self)

        self.prefs = prefs
        self.type_specific_widgets = []
        self.current_vbox_height_offset = 0
        self.values = {
            "command": commands.create_simple,
            "name": "",
            "ctype": "",
            "dead": False,
            "foreign": False,
            "groups": [],
            "serialize": ['name', 'ctype']
        }

        self.setupUi(self)

        self.typeSelect.currentTextChanged.connect(lambda text: self.set_value("ctype", text))
        self.characterName.textChanged.connect(lambda text: self.set_value("name", text))
        self.groupName.textChanged.connect(lambda text: self.set_value("groups", [text]))
        self.foreignBox.toggled.connect(self.set_foreign)
        self.foreignText.textChanged.connect(self.set_foreign)
        self.deceasedBox.toggled.connect(self.set_deceased)
        self.deceasedText.textChanged.connect(self.set_deceased)

        self.typeSelect.currentIndexChanged.connect(self.update_type_specific_controls)
        type_keys = self.prefs.get("type_paths", {}).keys()
        for type_key in sorted(type_keys):
            item = self.typeSelect.addItem(type_key.title(), userData=type_key)

    def set_value(self, key, value):
        self.values[key] = value

    def set_foreign(self, _):
        if self.foreignBox.isChecked():
            self.set_value("foreign", self.foreignText.text())
        else:
            self.set_value("foreign", False)

    def set_deceased(self, _=None):
        if self.deceasedBox.isChecked():
            self.set_value("dead", self.deceasedText.toPlainText())
        else:
            self.set_value("dead", False)

    def update_type_specific_controls(self, index):
        for widget in self.type_specific_widgets:
            self.infoForm.labelForField(widget).deleteLater()
            widget.deleteLater()
        self.type_specific_widgets = []

        def new_row(index, title, widget):
            self.infoForm.insertRow(index, title, widget)
            self.type_specific_widgets.append(widget)
            return widget.height()

        new_vbox_height_offset = 0
        type_key = self.typeSelect.itemData(index)
        if type_key == 'changeling':
            seeming_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(2, '&Seeming', seeming_select)
            kith_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(3, '&Kith', kith_select)
            courtInput = QtWidgets.QLineEdit(self)
            new_vbox_height_offset += new_row(4, '&Court', courtInput)

            def update_kiths(index=0):
                kith_select.clear()
                kith_select.addItems(seeming_select.currentData())

            seeming_select.currentIndexChanged.connect(update_kiths)
            seeming_select.currentTextChanged.connect(lambda text: self.set_value('seeming', text))
            kith_select.currentTextChanged.connect(lambda text: self.set_value('kith', text))
            courtInput.textChanged.connect(lambda text: self.set_value("court", text))

            for seeming in self.prefs.get('changeling.seemings'):
                seeming_select.addItem(seeming.title(), userData=[kith.title() for kith in self.prefs.get('changeling.kiths.{}'.format(seeming))])

            self.set_value("command", commands.create_changeling)
            self.set_value("serialize", ['name', 'seeming', 'kith'])
        else:
            self.set_value("command", commands.create_simple)
            self.set_value("serialize", ['name', 'ctype'])

        new_vbox_height_offset += len(self.type_specific_widgets)*6

        self.verticalLayoutWidget.resize(
            self.verticalLayoutWidget.width(),
            self.verticalLayoutWidget.height() - self.current_vbox_height_offset + new_vbox_height_offset)
        self.current_vbox_height_offset = new_vbox_height_offset

        self.adjustSize()

    def run(self):
        self.characterName.setFocus()
        result = self.exec_()
        return result == self.Accepted and self.values['name']
