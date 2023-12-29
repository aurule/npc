from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QToolBar, QStatusBar, QWidget
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon

from .. import resources

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NPC Campaign Manager")
        self.setMinimumSize(QSize(400, 300))

        self.init_actions()
        self.init_toolbar()

        table_tabs = QTabWidget()
        characters_tab = QWidget()
        table_tabs.addTab(characters_tab, "Characters")
        self.setCentralWidget(table_tabs)

        self.setStatusBar(QStatusBar(self))

    def init_actions(self):
        self.actions = {}
        # create and save our actions for later use

    def init_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)
        # add whatever actions and menus we need
