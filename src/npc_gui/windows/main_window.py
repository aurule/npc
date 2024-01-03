from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QToolBar, QStatusBar,
    QMenuBar, QMenu, QApplication, QTableView, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QFileDialog, QMessageBox, QPushButton, QSizePolicy
)
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QAction, QIcon, QDesktopServices

from ..models import CharactersTableModel
from ..helpers import theme_or_resource_icon
from ..widgets import ActionButton
from . import NewCampaignDialog
from npc import campaign
from npc import __version__ as npc_version
from npc.settings import app_settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NPC Campaign Manager")
        self.setMinimumSize(QSize(400, 300))

        self.init_actions()
        self.init_menus()
        self.init_toolbar()

        self.init_hello()

        self.setStatusBar(QStatusBar(self))

    def init_actions(self):
        self.actions = {}

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.exit_app)
        exit_action.setIcon(theme_or_resource_icon("application-exit"))
        exit_action.setStatusTip("Quit NPC")
        self.actions["exit"] = exit_action

        open_action = QAction("&Open Campaign...", self)
        open_action.triggered.connect(self.open_campaign)
        open_action.setIcon(theme_or_resource_icon("folder-open"))
        open_action.setStatusTip("Open an existing campaign")
        open_action.setShortcut("ctrl+o")
        self.actions["open"] = open_action

        new_action = QAction("New Campaign...", self)
        new_action.triggered.connect(self.new_campaign)
        new_action.setIcon(theme_or_resource_icon("folder-new"))
        new_action.setStatusTip("Set up a new campaign")
        self.actions["new"] = new_action

        docs_action = QAction("Browse Web &Documentation", self)
        docs_action.triggered.connect(self.browse_docs)
        docs_action.setIcon(theme_or_resource_icon("emblem-symbolic-link"))
        docs_action.setStatusTip("Open the web documentation in your browser")
        self.actions["docs"] = docs_action

        about_action = QAction("&About NPC", self)
        about_action.triggered.connect(self.about)
        about_action.setStatusTip("Show information about NPC")
        self.actions["about"] = about_action

        about_qt_action = QAction("&Qt Info", self)
        about_qt_action.triggered.connect(self.about_qt)
        about_qt_action.setStatusTip("Show information about the Qt framework")
        self.actions["qt_info"] = about_qt_action

    def init_menus(self):
        menubar = QMenuBar()

        file_menu = QMenu("&File")
        file_menu.addAction(self.actions.get("new"))
        file_menu.addAction(self.actions.get("open"))
        file_menu.addSeparator()
        file_menu.addAction(self.actions.get("exit"))
        menubar.addMenu(file_menu)

        help_menu = QMenu("&Help")
        help_menu.addAction(self.actions.get("docs"))
        help_menu.addAction(self.actions.get("about"))
        help_menu.addAction(self.actions.get("qt_info"))
        menubar.addMenu(help_menu)

        self.setMenuBar(menubar)

    def init_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

    def init_hello(self):
        hello_container = QWidget()
        welcome_layout = QVBoxLayout(hello_container)

        title_label = QLabel("NPC Campaign Manager")
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(18)
        title_label.setFont(font)
        title_sizing = QSizePolicy()
        title_sizing.setVerticalPolicy(QSizePolicy.Fixed)
        title_sizing.setHorizontalPolicy(QSizePolicy.Expanding)
        title_label.setSizePolicy(title_sizing)
        welcome_layout.addWidget(title_label)

        button_layout = QHBoxLayout()
        open_button = ActionButton(self.actions.get("open"))
        button_layout.addWidget(open_button)
        new_button = ActionButton(self.actions.get("new"))
        button_layout.addWidget(new_button)
        welcome_layout.addLayout(button_layout)

        # recent campaigns with a clickable list, each preceded by a folder icon

        self.setCentralWidget(hello_container)

    def exit_app(self, _parent):
        QApplication.quit()

    def browse_docs(self, _parent):
        QDesktopServices.openUrl(QUrl("https://npc.readthedocs.io/en/stable/"))

    @property
    def campaign(self):
        return QApplication.instance().campaign

    @property
    def settings(self):
        return QApplication.instance().settings

    def open_campaign(self, _parent):
        target = QFileDialog.getExistingDirectory(self, "Open Campaign")
        if target:
            self.load_campaign_dir(target)

    def load_campaign_dir(self, campaign_path):
        campaign_root = campaign.find_campaign_root(campaign_path)
        if not campaign_root:
            QMessageBox.critical(self, "No Campaign", f"The folder {campaign_path} is not an NPC campaign, nor are any of its parent directories.")
            return

        app = QApplication.instance()
        app.campaign = campaign.Campaign(campaign_root)
        # outdated and migrations?

        app.campaign.characters.refresh()
        self.init_tables()

    def init_tables(self):
        table_tabs = QTabWidget()

        characters_tab = QWidget()
        characters_layout = QVBoxLayout(characters_tab)

        characters_model = CharactersTableModel(
            self.campaign.characters,
            ["realname", "mnemonic", "type", "location"]
        )
        characters_table = QTableView()
        characters_table.verticalHeader().hide()
        characters_table.setCornerButtonEnabled(False)
        characters_table.setSortingEnabled(True)
        characters_table.setModel(characters_model)
        characters_table.sortByColumn(0, Qt.AscendingOrder)
        characters_layout.addWidget(characters_table)
        table_tabs.addTab(characters_tab, "Characters")

        self.setCentralWidget(table_tabs)

    def new_campaign(self, _parent):
        campaign_path = QFileDialog.getExistingDirectory(self, "Choose campaign directory")
        if not campaign_path:
            return

        picker = NewCampaignDialog(campaign_path, parent=self)
        if picker.exec():
            npc.campaign.init(
                picker.campaign_path,
                name=picker.campaign_name,
                desc=picker.campaign_desc.strip(),
                system=picker.campaign_system,
                settings=app_settings()
            )
            self.load_campaign_dir(picker.campaign_path)

    def about(self, _parent):
        QMessageBox.about(
            self,
            "About NPC",
            f"<h1>NPC {npc_version}</h1>\
            <p>NPC Campaign Manager is copyright 2023 Paige Andrews. It is made available under the MIT license.</p>"
        )

    def about_qt(self, _parent):
        QMessageBox.aboutQt(self)
