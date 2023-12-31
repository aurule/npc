from PySide6.QtGui import QIcon

from . import resources

def theme_or_resource_icon(name: str) -> QIcon:
    return QIcon.fromTheme(name, QIcon(f":/icons/{name}"))
