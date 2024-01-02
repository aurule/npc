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

    def open_campaign(self, _parent):
        target = QFileDialog.getExistingDirectory(self, "Open Campaign")
        if target:
            self.load_campaign_dir(target)

    def load_campaign_dir(campaign_path):
        campaign_root = campaign.find_campaign_root(target)
        if not campaign_root:
            QMessageBox.critical(self, "No Campaign", f"The folder {target} is not an NPC campaign, nor are any of its parent directories.")
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
        characters_table.setModel(characters_model)
        characters_table.verticalHeader().hide()
        characters_layout.addWidget(characters_table)
        table_tabs.addTab(characters_tab, "Characters")

        self.setCentralWidget(table_tabs)

    def new_campaign(self, _parent):
        campaign_path = QFileDialog.getExistingDirectory(self, "Open Campaign")
        if not campaign_path:
            return

        picker = NewCampaignDialog(campaign_path, parent=self)
        if picker.exec():
            print(picker.campaign_path)
            print(picker.campaign_name)
            print(picker.campaign_system)
            print(picker.campaign_desc)
            # get dir, name, sys, desc from modal
            # set up!
            # npc.campaign.init(
            #     campaign_path,
            #     name=name,
            #     desc=desc,
            #     system=system,
            #     settings=settings)
            # self.load_campaign_dir(selected_dir)
