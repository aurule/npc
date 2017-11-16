from PyQt5 import QtCore, QtGui, QtWidgets
from contextlib import contextmanager
from os import chdir, path, getcwd

import npc
from npc import commands, util, settings
from npc.__version__ import __version__

from .new_character import NewCharacterDialog
from .init_dialog import InitDialog
from .uis.about import Ui_AboutDialog
from .uis.main_window import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    """
    Show and run the GUI

    This class handles all the management of the campaign, including showing
    dialogs and running commands.
    """
    def __init__(self, window, prefs, campaign=None):
        Ui_MainWindow.__init__(self)

        self.prefs = prefs
        self.campaign_root = path.expanduser('~')

        self.init_main_window(window)
        self.init_menus()
        self.init_table()
        self.init_about_window()
        self.init_command_actions()

        # quit menu entry
        self.actionQuit.triggered.connect(self.quit)

        if campaign is not None:
            self.set_campaign_root(campaign)

    def init_main_window(self, window):
        """Initialize the main window object"""
        self.window = window
        self.setupUi(window)
        self.init_main_widgets()
        self.force_titles()

    def init_main_widgets(self):
        """Connect the main window widgets together"""
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(350)
        self.timer.timeout.connect(self.update_table)
        self.characterSearch.textEdited.connect(self.timer.start)

        self.character_table_model = CharacterTableModel(self)
        self.characterTableView.setModel(self.character_table_model)

        self.open_character_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Return"),
            self.characterTableView,
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.open_character_shortcut.activated.connect(self.open_multiple_characters)

        self.characterCount = QtWidgets.QLabel()
        self.window.statusBar().addWidget(self.characterCount)
        self.characterTableView.doubleClicked.connect(self.open_character)

        self.focus_search_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+L"),
            self.window,
            context=QtCore.Qt.WindowShortcut)
        self.focus_search_shortcut.activated.connect(self.characterSearch.setFocus)

        self.recentCampaignActions = [QtWidgets.QAction(self.menuOpen_Recent_Campaign, visible=False, triggered=self.open_recent_campaign) for i in range(5)]
        for act in self.recentCampaignActions:
            self.menuOpen_Recent_Campaign.addAction(act)

    def init_menus(self):
        """Set up menus"""
        self.update_recent_campaigns()

    def init_table(self):
        """Set up main table"""
        self.table_header = self.characterTableView.horizontalHeader()
        self.table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.update_table()

    def init_about_window(self):
        """Set up about window"""
        self.about_dialog = QtWidgets.QDialog(self.window)
        AboutDialog(self.about_dialog)
        self.actionAbout.triggered.connect(self.about_dialog.open)

    def init_command_actions(self):
        """Link up actions with the right command methods"""
        self.actionOpenCampaign.triggered.connect(self.open_campaign)
        self.actionUserSettings.triggered.connect(self.run_user_settings)
        self.actionCampaignSettings.triggered.connect(self.run_campaign_settings)
        self.actionReloadSettings.triggered.connect(self.run_reload_settings)
        self.actionInit.triggered.connect(self.run_init)
        self.actionNew_Character.triggered.connect(self.run_new_character)
        self.actionNew_Session.triggered.connect(self.run_new_session)

    def update_recent_campaigns(self):
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
        QtWidgets.QMessageBox.warning(parent, title, message, QtWidgets.QMessageBox.Ok)

    def update_table(self):
        """Update the characters table using search results"""
        search_rules = self.characterSearch.text().split(';')
        all_characters = list(npc.parser.get_characters())
        filtered_characters = npc.commands.find_characters(search_rules, all_characters)

        self.character_table_model.update_data(filtered_characters)
        self.characterTableView.resizeColumnsToContents()

        if len(all_characters) == len(filtered_characters):
            status_text = "{} characters".format(len(all_characters))
        else:
            status_text = "{} of {} characters".format(len(filtered_characters), len(all_characters))
        self.characterCount.setText(status_text)

    def open_character(self, index):
        """Open a character based on its index in the table"""
        char = self.character_table_model.characters[index.row()]
        util.open_files(char.get('path'), prefs=self.prefs)

    def open_multiple_characters(self):
        """Open multiple characters from the index selection"""
        indexes = self.characterTableView.selectedIndexes()
        characters = [self.character_table_model.characters[i.row()].get('path') for i in indexes]
        util.open_files(*characters, prefs=self.prefs)

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
            str(QtCore.QStandardPaths.StandardLocation(QtCore.QStandardPaths.DocumentsLocation)))
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

        Args:
            root_dir (str): Root directory of the campaign folder to load
        """
        root_dir = path.expanduser(root_dir)
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
        campaign_titles.insert(0, self.prefs.get('campaign_name'))
        del campaigns[5:]
        del campaign_titles[5:]

        settings.setValue('recentCampaigns/paths', campaigns)
        settings.setValue('recentCampaigns/titles', campaign_titles)
        self.update_recent_campaigns()
        self.update_table()

    @contextmanager
    def safe_command(self, command):
        """
        Helper to show error dialog for AttributeErrors from commands

        Args:
            command (callable): The command to run. Any AttributeError will
                result in an error dialog being shown

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
            dialog_class (Class): The dialog class to instantiate
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

            util.open_files(*result.openable, prefs=self.prefs)

    def run_campaign_settings(self):
        """Run the campaign settings command"""
        with self.safe_command(commands.open_settings) as command:
            result = command('campaign', show_defaults=True, prefs=self.prefs)

            if not result.success:
                self._show_error('Could not open campaign settings', result.errmsg)
                return

            util.open_files(*result.openable, prefs=self.prefs)

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
        self.window.setWindowTitle("NPC - {}".format(self.prefs.get('campaign_name')))

    def run_new_session(self):
        """Run the session command"""
        with self.safe_command(commands.session) as command:
            result = command(prefs=self.prefs)

            if not result.success:
                self._show_error('Could not create session files', result.errmsg)
                return

            util.open_files(*result.openable, prefs=self.prefs)

    def run_init(self):
        """Run the init command with inputs from its dialog"""
        with self.dialog(InitDialog, self.window, self.prefs) as init_dialog:
            if path.exists(self.prefs.get_settings_path('campaign')):
                init_dialog.set_campaign_name(self.prefs.get('campaign_name'), enabled=False)
            else:
                init_dialog.set_campaign_name(path.basename(getcwd()))

            if init_dialog.run():
                values = init_dialog.values
                with self.safe_command(commands.init) as command:
                    command(**values)

    def run_new_character(self):
        """Run the new character command"""
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
        """Quite the application"""
        QtCore.QCoreApplication.instance().quit()

class AboutDialog(Ui_AboutDialog):
    """The static About dialog"""

    def __init__(self, dialog):
        Ui_AboutDialog.__init__(self)
        self.setupUi(dialog)
        self.labelVersion.setText("Version {0}".format(__version__))

class CharacterTableModel(QtCore.QAbstractTableModel):
    """Model for character data"""
    def __init__(self, parent=None):
        super(CharacterTableModel, self).__init__()
        self.characters = []
        self.column_header_tags = [
            "name",
            "type"
        ]
        self.column_header_names =[
            "Name",
            "Type"
        ]

    def update_data(self, new_chars):
        """
        Update the table with new data

        Args:
            new_chars (list): List of character objects to show in the table
        """
        self.beginResetModel()
        self.characters = new_chars
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Get the number of rows in the table"""
        return len(self.characters)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Get the number of columns in the table"""
        return len(self.column_header_tags)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Get the data to show in a table cell"""
        if role == QtCore.Qt.DisplayRole:
            tag = self.column_header_tags[index.column()]
            return self.characters[index.row()].get_first(tag)
        else:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Get header titles"""
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.column_header_names[section]
        else:
            return QtCore.QVariant()
