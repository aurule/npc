from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import QEventLoop

class LoadingBar(QProgressBar):
    def __init__(self, max_value: int, parent = None):
        super().__init__(parent = parent)

        self.setMinimum(0)
        self.setMaximum(max_value)
        self.setValue(0)

    def next(self):
        self.setValue(self.value() + 1)
