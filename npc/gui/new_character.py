from PyQt5 import QtCore, QtGui, QtWidgets

from npc import commands
from .uis.new_character import Ui_NewCharacterDialog

class NewCharacterDialog(QtWidgets.QDialog, Ui_NewCharacterDialog):
    def __init__(self, parent, prefs):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_NewCharacterDialog.__init__(self)

        self.prefs = prefs
        self.type_specific_widgets = []
        self.current_vbox_height_offset = 0
        self.values = {
            "command": commands.create_simple,
            "name": "",
            "ctype": "",
            "dead": False,
            "foreign": False,
            "groups": [],
            "serialize": ['name', 'ctype']
        }

        self.setupUi(self)

        self.typeSelect.currentTextChanged.connect(lambda text: self.set_value("ctype", text))
        self.characterName.textChanged.connect(lambda text: self.set_value("name", text))
        self.groupName.textChanged.connect(lambda text: self.set_value("groups", [text]))
        self.foreignBox.toggled.connect(self.set_foreign)
        self.foreignText.textChanged.connect(self.set_foreign)
        self.deceasedBox.toggled.connect(self.set_deceased)
        self.deceasedText.textChanged.connect(self.set_deceased)

        self.typeSelect.currentIndexChanged.connect(self.update_type_specific_controls)
        type_keys = self.prefs.get("type_paths", {}).keys()
        for type_key in sorted(type_keys):
            item = self.typeSelect.addItem(type_key.title(), userData=type_key)

    def set_value(self, key, value):
        self.values[key] = value

    def set_foreign(self, _):
        if self.foreignBox.isChecked():
            self.set_value("foreign", self.foreignText.text())
        else:
            self.set_value("foreign", False)

    def set_deceased(self, _=None):
        if self.deceasedBox.isChecked():
            self.set_value("dead", self.deceasedText.toPlainText())
        else:
            self.set_value("dead", False)

    def update_type_specific_controls(self, index):
        for widget in self.type_specific_widgets:
            self.infoForm.labelForField(widget).deleteLater()
            widget.deleteLater()
        self.type_specific_widgets = []

        def new_row(index, title, widget):
            self.infoForm.insertRow(index, title, widget)
            self.type_specific_widgets.append(widget)
            return widget.height()

        new_vbox_height_offset = 0
        type_key = self.typeSelect.itemData(index)
        if type_key == 'changeling':
            seeming_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(2, '&Seeming', seeming_select)
            kith_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(3, '&Kith', kith_select)
            courtInput = QtWidgets.QLineEdit(self)
            new_vbox_height_offset += new_row(4, '&Court', courtInput)

            def update_kiths(index=0):
                kith_select.clear()
                kith_select.addItems(seeming_select.currentData())

            seeming_select.currentIndexChanged.connect(update_kiths)
            seeming_select.currentTextChanged.connect(lambda text: self.set_value('seeming', text))
            kith_select.currentTextChanged.connect(lambda text: self.set_value('kith', text))
            courtInput.textChanged.connect(lambda text: self.set_value("court", text))

            for seeming in self.prefs.get('changeling.seemings'):
                seeming_select.addItem(seeming.title(), userData=[kith.title() for kith in self.prefs.get('changeling.kiths.{}'.format(seeming))])

            self.set_value("command", commands.create_changeling)
            self.set_value("serialize", ['name', 'seeming', 'kith'])
        else:
            self.set_value("command", commands.create_simple)
            self.set_value("serialize", ['name', 'ctype'])

        new_vbox_height_offset += len(self.type_specific_widgets)*6

        self.verticalLayoutWidget.resize(
            self.verticalLayoutWidget.width(),
            self.verticalLayoutWidget.height() - self.current_vbox_height_offset + new_vbox_height_offset)
        self.current_vbox_height_offset = new_vbox_height_offset

        self.adjustSize()

    def run(self):
        self.characterName.setFocus()
        result = self.exec_()
        return result == self.Accepted and self.values['name']
