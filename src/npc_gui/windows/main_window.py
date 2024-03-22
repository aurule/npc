from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QToolBar, QStatusBar,
    QMenuBar, QMenu, QApplication, QTableView, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QFileDialog, QMessageBox, QPushButton, QSizePolicy,
    QFormLayout
)
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QAction, QIcon, QDesktopServices

import click

from ..helpers import fetch_icon, find_settings_file
from ..widgets import ActionButton, ResourceTable
from ..widgets.size_policies import *
from ..util import RecentCampaigns
from . import (
    NewCampaignDialog, NewCharacterDialog, SettingsOutdatedDialog,
    SettingsMigrationPrompt, PostMigrationDialog
)
import npc
from npc import campaign
from npc import __version__ as npc_version
from npc.settings import app_settings
from npc.settings.migrations import SettingsMigrator

class MainWindow(QMainWindow):
    def __init__(self, campaign_dir: str = None):
        super().__init__()

        self.campaign: Campaign = None
        self.default_settings: Settings = app_settings()
        self.recent_campaigns: RecentCampaigns = RecentCampaigns()

        self.campaign_actions: list[QAction] = []
        self.actions: dict[str, QAction] = {}

        self.setWindowTitle(self.tr("NPC Campaign Manager"))
        self.setMinimumSize(QSize(700, 600))

        self.init_actions()
        self.init_menus()
        self.init_toolbar()

        self.init_recent_campaigns()
        self.init_hello()

        self.setStatusBar(QStatusBar(self))

        self.update_campaign_availability()

        self.warn_if_outdated("user")
        self.try_settings_migration("user", on_rejected = self.exit_app)

        if campaign_dir:
            self.load_campaign_dir(campaign_dir)

    def init_actions(self):
        # General actions

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.exit_app)
        exit_action.setIcon(fetch_icon("application-exit"))
        exit_action.setStatusTip("Quit NPC")
        self.actions["exit"] = exit_action

        # Campaign actions

        open_action = QAction("&Open Campaign...", self)
        open_action.triggered.connect(self.open_campaign)
        open_action.setIcon(fetch_icon("folder-open"))
        open_action.setStatusTip("Open an existing campaign")
        open_action.setShortcut("ctrl+o")
        self.actions["open"] = open_action

        clear_recent = QAction("Clear Items")
        clear_recent.triggered.connect(self.clear_recent_campaigns)
        clear_recent.setStatusTip("Clear recent campaigns")
        self.actions["clear_recent"] = clear_recent

        new_action = QAction("&New Campaign...", self)
        new_action.triggered.connect(self.new_campaign)
        new_action.setIcon(fetch_icon("folder-new"))
        new_action.setStatusTip("Set up a new campaign")
        self.actions["new"] = new_action

        close_action = QAction("&Close Campaign", self)
        close_action.triggered.connect(self.close_campaign)
        close_action.setStatusTip("Close the current campaign")
        self.actions["close"] = close_action
        self.campaign_actions.append("close")

        refresh_action = QAction("&Refresh", self)
        refresh_action.triggered.connect(self.refresh_campaign)
        refresh_action.setStatusTip("Reload campaign info and characters")
        refresh_action.setShortcut("ctrl+r")
        refresh_action.setIcon(fetch_icon("view-refresh"))
        self.actions["refresh"] = refresh_action
        self.campaign_actions.append("refresh")

        # Character actions

        new_character = QAction("New Character...")
        new_character.triggered.connect(self.new_character)
        new_character.setIcon(fetch_icon("document-new"))
        new_character.setStatusTip("Create a new character")
        new_character.setShortcut("ctrl+n")
        self.actions["new_character"] = new_character
        self.campaign_actions.append("new_character")

        open_character = QAction("Open in editor")
        open_character.triggered.connect(self.open_character)
        open_character.setIcon(fetch_icon("document-edit"))
        open_character.setStatusTip("Open the selected character(s) in your text editor")
        open_character.setShortcut("ctrl+e")
        open_character.setDisabled(True)
        self.actions["open_character"] = open_character

        # Session actions

        session_new = QAction("Next session", self)
        session_new.triggered.connect(self.make_session)
        session_new.setStatusTip("Create and open the next set of session and plot files")
        session_new.setIcon(fetch_icon("go-next"))
        self.actions["session"] = session_new
        self.campaign_actions.append("session")

        session_latest = QAction("Open latest files", self)
        session_latest.triggered.connect(self.latest_all)
        session_latest.setStatusTip("Open the most recent plot and session files")
        self.actions["session_latest"] = session_latest
        self.campaign_actions.append("session_latest")

        session_latest_session = QAction("Open latest session file", self)
        session_latest_session.triggered.connect(self.latest_session)
        session_latest_session.setStatusTip("Open the most recent session file")
        self.actions["session_latest_session"] = session_latest_session
        self.campaign_actions.append("session_latest_session")

        session_latest_plot = QAction("Open latest plot file", self)
        session_latest_plot.triggered.connect(self.latest_plot)
        session_latest_plot.setStatusTip("Open the most recent plot file")
        self.actions["session_latest_plot"] = session_latest_plot
        self.campaign_actions.append("session_latest_plot")

        # Help actions

        docs_action = QAction("Browse Web &Documentation", self)
        docs_action.triggered.connect(self.browse_docs)
        docs_action.setIcon(fetch_icon("emblem-symbolic-link"))
        docs_action.setStatusTip("Open the web documentation in your browser")
        self.actions["docs"] = docs_action

        about_action = QAction("&About NPC", self)
        about_action.triggered.connect(self.about)
        about_action.setStatusTip("Show information about NPC")
        about_action.setIcon(fetch_icon("help-about"))
        self.actions["about"] = about_action

        about_qt_action = QAction("About &Qt", self)
        about_qt_action.triggered.connect(self.about_qt)
        about_qt_action.setStatusTip("Show information about the Qt framework")
        self.actions["qt_info"] = about_qt_action

        # Settings commands

        settings_user = QAction("Browse User &Settings", self)
        settings_user.triggered.connect(self.settings_user)
        settings_user.setStatusTip("Open your user settings directory")
        self.actions["settings_user"] = settings_user

        settings_campaign = QAction("Browse Campaign &Settings", self)
        settings_campaign.triggered.connect(self.settings_campaign)
        settings_campaign.setStatusTip("Open this campaign's settings directory")
        self.actions["settings_campaign"] = settings_campaign
        self.campaign_actions.append("settings_campaign")

    def init_menus(self):
        menubar = QMenuBar()

        file_menu = QMenu("&File")
        file_menu.addAction(self.actions.get("new_character"))
        file_menu.addAction(self.actions.get("open_character"))
        file_menu.addSeparator()
        file_menu.addAction(self.actions.get("new"))
        file_menu.addAction(self.actions.get("open"))
        self.recent_campaigns_menu = QMenu("Open &Recent")
        file_menu.addMenu(self.recent_campaigns_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.actions.get("close"))
        file_menu.addSeparator()
        file_menu.addAction(self.actions.get("exit"))
        menubar.addMenu(file_menu)

        session_menu = QMenu("&Session")
        session_menu.addAction(self.actions.get("session"))
        session_menu.addSeparator()
        session_menu.addAction(self.actions.get("session_latest"))
        session_menu.addAction(self.actions.get("session_latest_session"))
        session_menu.addAction(self.actions.get("session_latest_plot"))
        menubar.addMenu(session_menu)

        settings_menu = QMenu("Setti&ngs")
        settings_menu.addAction(self.actions.get("settings_user"))
        settings_menu.addAction(self.actions.get("settings_campaign"))
        menubar.addMenu(settings_menu)

        help_menu = QMenu("&Help")
        help_menu.addAction(self.actions.get("docs"))
        help_menu.addSeparator()
        help_menu.addAction(self.actions.get("qt_info"))
        help_menu.addAction(self.actions.get("about"))
        menubar.addMenu(help_menu)

        self.setMenuBar(menubar)

    def init_recent_campaigns(self):
        self.actions["recent_campaigns"] = [self.make_recent_campaign_action(c) for c in reversed(self.recent_campaigns.campaigns())]
        self.recent_campaigns_menu.clear()

        if self.recent_campaigns:
            for action in self.actions.get("recent_campaigns"):
                self.recent_campaigns_menu.addAction(action)
            self.recent_campaigns_menu.addSeparator()
            self.recent_campaigns_menu.addAction(self.actions.get("clear_recent"))
        else:
            none_action = QAction("No recent campaigns", self)
            none_action.setDisabled(True)
            self.recent_campaigns_menu.addAction(none_action)

    def make_recent_campaign_action(self, campaign_info: dict) -> QAction:
        name = campaign_info.get("name")
        path = campaign_info.get("path")
        action = QAction(f"{name} ({path})", self)
        action.triggered.connect(lambda: self.load_campaign_dir(path))
        action.setStatusTip(f"Open {name}")
        return action

    def init_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.addAction(self.actions.get("session"))
        toolbar.addAction(self.actions.get("new_character"))
        toolbar.addAction(self.actions.get("refresh"))
        self.addToolBar(toolbar)

    def init_hello(self):
        hello_container = QWidget()
        welcome_layout = QVBoxLayout(hello_container)
        welcome_layout.addSpacing(20)

        title_label = QLabel("NPC Campaign Manager")
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(18)
        title_label.setFont(font)
        title_sizing = QSizePolicy()
        title_sizing.setHorizontalPolicy(QSizePolicy.Expanding)
        title_label.setSizePolicy(title_sizing)
        welcome_layout.addWidget(title_label)
        welcome_layout.addSpacing(20)

        button_layout = QHBoxLayout()
        open_button = ActionButton(self.actions.get("open"))
        button_layout.addWidget(open_button)
        new_button = ActionButton(self.actions.get("new"))
        button_layout.addWidget(new_button)
        welcome_layout.addLayout(button_layout)

        welcome_layout.addSpacing(20)

        hello_recent_buttons = QFormLayout()
        recents_label = QLabel("Recent Campaigns")
        font = recents_label.font()
        font.setPointSize(14)
        recents_label.setFont(font)
        hello_recent_buttons.addWidget(recents_label)
        if self.recent_campaigns:
            for action in self.actions.get("recent_campaigns"):
                recent_button = ActionButton(action)
                hello_recent_buttons.addWidget(recent_button)
        else:
            no_recents = QLabel("No recent campaigns")
            no_recents.setDisabled(True)
            hello_recent_buttons.addWidget(no_recents)
        welcome_layout.addLayout(hello_recent_buttons)

        self.setCentralWidget(hello_container)

    def exit_app(self, _parent = None):
        QApplication.quit()

    def browse_docs(self, _parent):
        QDesktopServices.openUrl(QUrl("https://npc.readthedocs.io/en/stable/"))

    @property
    def settings(self):
        if self.campaign:
            return self.campaign.settings
        return self.default_settings

    def warn_if_outdated(self, location: str):
        if self.settings.package_outdated(location):
            outdated_dialog = SettingsOutdatedDialog(self.settings, location, self)
            outdated_dialog.open()

    def try_settings_migration(self, location: str, on_rejected = None):
        def do_migrate():
            messages = migrator.migrate(location)
            post_migration = PostMigrationDialog(location, messages, self)
            post_migration.open()

        migrator = SettingsMigrator(self.settings)
        if migrator.can_migrate(location):
            migrate_dialog = SettingsMigrationPrompt(migrator, location, self)
            migrate_dialog.accepted.connect(do_migrate)
            if on_rejected:
                migrate_dialog.rejected.connect(on_rejected)
            migrate_dialog.open()

    def open_campaign(self, _parent):
        target = QFileDialog.getExistingDirectory(self, "Open Campaign")
        if target:
            self.load_campaign_dir(target)

    def load_campaign_dir(self, campaign_path: str):
        db = npc.db.DB()
        db.reset()
        campaign_root = campaign.find_campaign_root(campaign_path)
        if not campaign_root:
            QMessageBox.critical(
                self,
                "No Campaign",
                f"The folder {campaign_path} is not an NPC campaign, nor are any of its parent directories."
            )
            return

        self.campaign = campaign.Campaign(campaign_root)
        self.setWindowTitle(f"{self.campaign.name} | NPC")
        self.warn_if_outdated("campaign")
        self.try_settings_migration("campaign", on_rejected = self.close_campaign)

        self.campaign.characters.seed()
        self.recent_campaigns.add(self.campaign)
        self.init_recent_campaigns()
        self.init_tables()
        self.update_campaign_availability()


    def update_campaign_availability(self):
        campaign_available = self.campaign != None
        for action_key in self.campaign_actions:
            self.actions.get(action_key).setEnabled(campaign_available)

    def init_tables(self):
        table_tabs = QTabWidget()

        characters_tab = QWidget()
        characters_layout = QVBoxLayout(characters_tab)
        columns = self.settings.get("gui.columns.characters")
        self.characters_table = ResourceTable(
            self.campaign.characters,
            columns
        )
        self.characters_table.selectionModel().selectionChanged.connect(self.update_character_selection)
        characters_layout.addWidget(self.characters_table)

        character_actions_bar = QWidget()
        character_actions_layout = QHBoxLayout(character_actions_bar)

        self.open_character_button = ActionButton(self.actions.get("open_character"))
        self.open_character_button.setSizePolicy(fixed_both)
        character_actions_layout.addWidget(self.open_character_button)

        self.characters_count_label = QLabel(f"{self.characters_table.model.rowCount()} characters")
        self.characters_count_label.setAlignment(Qt.AlignCenter)
        character_actions_layout.addWidget(self.characters_count_label)

        new_character_button = ActionButton(self.actions.get("new_character"))
        new_character_button.setSizePolicy(fixed_both)
        character_actions_layout.addWidget(new_character_button)

        characters_layout.addWidget(character_actions_bar)

        table_tabs.addTab(characters_tab, "Characters")

        self.setCentralWidget(table_tabs)

    def refresh_campaign(self, _parent):
        self.campaign.characters.refresh()
        self.characters_table.model.reload()

    def new_campaign(self, _parent):
        campaign_path = QFileDialog.getExistingDirectory(self, "Choose campaign directory")
        if not campaign_path:
            return

        picker = NewCampaignDialog(campaign_path, parent=self)
        if picker.exec():
            campaign.init(
                picker.campaign_path,
                name=picker.campaign_name,
                desc=picker.campaign_desc.strip(),
                system=picker.campaign_system,
                settings=app_settings()
            )
            self.load_campaign_dir(picker.campaign_path)

    def close_campaign(self, _parent = None):
        self.campaign = None
        self.update_campaign_availability()
        self.init_hello()

    def clear_recent_campaigns(self, _parent):
        self.recent_campaigns.clear()
        self.init_recent_campaigns()
        if not self.campaign:
            self.init_hello()

    def about(self, _parent):
        QMessageBox.about(
            self,
            "About NPC",
            f"<h1>NPC {npc_version}</h1>\
            <p>NPC Campaign Manager is copyright 2023 Paige Andrews. It is made available under the MIT license.</p>"
        )

    def about_qt(self, _parent):
        QMessageBox.aboutQt(self)

    def make_session(self, _parent):
        new_files = self.campaign.bump_planning_files()

        npc.util.edit_files(new_files.values(), settings = self.settings)

    def latest_session(self, _parent):
        self.open_latest("session")

    def latest_plot(self, _parent):
        self.open_latest("plot")

    def latest_all(self, _parent):
        self.open_latest("both")

    def open_latest(self, planning_type: str):
        if planning_type == "both":
            keys = ["plot", "session"]
        else:
            keys = [planning_type]

        files = [self.campaign.get_latest_planning_file(key) for key in keys]
        npc.util.edit_files(files, settings = self.settings)

    def settings_user(self, _parent):
        self.browse_settings("user")

    def settings_campaign(self, _parent):
        self.browse_settings("campaign")

    def browse_settings(self, location):
        target_file = find_settings_file(self.settings, location)
        click.launch(str(target_file), locate=True)

    def new_character(self, _parent):
        dialog = NewCharacterDialog(parent=self)
        if dialog.exec():
            self.campaign.characters.count += 1
            self.characters_table.model.reload()

    def open_character(self, _parent):
        selection = set(s.row() for s in self.characters_table.selectionModel().selectedIndexes())
        files = [self.characters_table.model.path_at(index) for index in selection]
        npc.util.edit_files(files, self.settings)

    def update_character_selection(self, selected, deselected):
        selection = set(s.row() for s in self.characters_table.selectionModel().selectedIndexes())
        total = len(selection)
        action = self.actions.get("open_character")
        action.setDisabled(not total)
        if total > 1:
            action.setText(f"Open {len(selection)} in editor")
        else:
            action.setText("Open in editor")
