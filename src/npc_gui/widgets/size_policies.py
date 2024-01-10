from PySide6.QtWidgets import QSizePolicy

fixed_horizontal = QSizePolicy()
fixed_horizontal.setHorizontalPolicy(QSizePolicy.Fixed)

fixed_vertical = QSizePolicy()
fixed_vertical.setVerticalPolicy(QSizePolicy.Fixed)

fixed_both = QSizePolicy()
fixed_both.setVerticalPolicy(QSizePolicy.Fixed)
fixed_both.setHorizontalPolicy(QSizePolicy.Fixed)
