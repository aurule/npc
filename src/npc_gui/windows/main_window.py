from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QToolBar, QStatusBar,
    QMenuBar, QMenu, QApplication, QTableView, QVBoxLayout,
    QLabel, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon

from ..models import CharactersTableModel
from ..helpers import theme_or_resource_icon
from npc import campaign

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NPC Campaign Manager")
        self.setMinimumSize(QSize(400, 300))

        self.init_actions()
        self.init_menus()
        self.init_toolbar()

        characters_model = CharactersTableModel()
        characters_table = QTableView()
        characters_table.setModel(characters_model)
        characters_table.verticalHeader().hide()
        characters_layout = QVBoxLayout()
        # characters_layout.addWidget(QLabel("Search bar goes here lol"))
        characters_layout.addWidget(characters_table)
        characters_tab = QWidget()
        characters_tab.setLayout(characters_layout)
        table_tabs = QTabWidget()
        table_tabs.addTab(characters_tab, "Characters")
        self.setCentralWidget(table_tabs)

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

    def init_menus(self):
        menubar = QMenuBar()

        file_menu = QMenu("&File")
        file_menu.addAction(self.actions.get("open"))
        file_menu.addSeparator()
        file_menu.addAction(self.actions.get("exit"))
        menubar.addMenu(file_menu)

        self.setMenuBar(menubar)

    def init_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

    def exit_app(self, _parent):
        QApplication.quit()

    def open_campaign(self, _parent):
        target = QFileDialog.getExistingDirectory(self, "Open Campaign")
        if not target:
            return

        campaign_root = campaign.find_campaign_root(target)
        if not campaign_root:
            QMessageBox.critical(self, "No Campaign", f"The folder {target} is not an NPC campaign, nor are any of its parent directories.")
            return

        app = QApplication.instance()
        app.campaign = campaign.Campaign(campaign_root)
        # outdated and migrations?
