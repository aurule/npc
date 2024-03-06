import platform

from PySide6.QtWidgets import QApplication

class NPCApplication(QApplication):
    """Core NPC GUI application class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if platform.system() == "Windows":
            self.setStyle("Fusion")
