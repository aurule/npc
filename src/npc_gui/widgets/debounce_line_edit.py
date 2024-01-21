from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import QTimer, Signal

class DebounceLineEdit(QLineEdit):
    debouncedText = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.emit_debounce)
        self.textChanged.connect(self.debounce_timer.start)
        self.setDebounceDelay(300)

    def setDebounceDelay(self, ms: int):
        self.debounce_timer.setInterval(ms)

    def emit_debounce(self):
        self.debouncedText.emit(self.text())
