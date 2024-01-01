from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QAction

class ActionButton(QPushButton):
    def __init__(self, action: QAction = None, parent: QWidget = None):
        super().__init__(parent=parent)
        self.action = None
        if action:
            self.setAction(action)

    def setAction(self, new_action: QAction):
        if self.action:
            self.action.changed.disconnect()
            self.clicked.disconnect()

        self.action = new_action

        self.update_status_from_action()
        self.action.changed.connect(self.update_status_from_action)
        self.clicked.connect(self.action.trigger)

    def update_status_from_action(self):
        if not self.action:
            return

        self.setText(self.action.text())
        self.setStatusTip(self.action.statusTip())
        self.setToolTip(self.action.toolTip())
        self.setIcon(self.action.icon())
        self.setEnabled(self.action.isEnabled())
        self.setCheckable(self.action.isCheckable())
        self.setChecked(self.action.isChecked())
