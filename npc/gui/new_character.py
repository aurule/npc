from PyQt5 import QtCore, QtGui, QtWidgets

from npc import commands
from .uis.new_character import Ui_NewCharacterDialog

class NewCharacterDialog(QtWidgets.QDialog, Ui_NewCharacterDialog):
    """Dialog for creating a new character"""

    def __init__(self, parent, prefs):
        """
        Create the new character dialog

        User inputs are stored in the dialog's `values` variable. They are
        updated immediately when the user makes a change.

        args:
            parent (QtWindow): Parent for the dialog
            prefs (Settings): Settings object to use for commands
        """

        QtWidgets.QDialog.__init__(self, parent)
        Ui_NewCharacterDialog.__init__(self)

        self.prefs = prefs
        self.type_specific_widgets = []
        self.current_vbox_height_offset = 0
        self.values = {
            "command": commands.create_character.standard,
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
        for type_key in sorted(self.prefs.get_available_types()):
            item = self.typeSelect.addItem(type_key.title(), userData=type_key)

    def set_value(self, key, value):
        """
        Set a value

        This helper is designed to be called from a Qt signal connection using a
        lambda.

        Args:
            key (str): Key to set
            value (varies): Value to store
        """

        self.values[key] = value

    def set_foreign(self, _):
        """Special handling for the compound `foreign` value"""

        if self.foreignBox.isChecked():
            self.set_value("foreign", self.foreignText.text())
        else:
            self.set_value("foreign", False)

    def set_deceased(self, _=None):
        """Special handling for the compound `deceased` value"""

        if self.deceasedBox.isChecked():
            self.set_value("dead", self.deceasedText.toPlainText())
        else:
            self.set_value("dead", False)

    def update_type_specific_controls(self, index):
        """
        Change the visible form fields based on the selected character type

        Args:
            index (int): Index of the type selection
        """

        for widget in self.type_specific_widgets:
            self.infoForm.labelForField(widget).deleteLater()
            widget.deleteLater()
        self.type_specific_widgets = []

        def new_row(index, title, widget):
            """
            Add a new row of controls to the form

            Args:
                index (int): Where to place the row in the form
                title (str): Label text for the row
                widget (QtWidget): Widget for the row

            Returns:
                The height of the row, as gotten from the widget
            """

            self.infoForm.insertRow(index, title, widget)
            self.type_specific_widgets.append(widget)
            return widget.height()

        new_vbox_height_offset = 0
        type_key = self.typeSelect.itemData(index)
        if type_key == 'changeling':
            seeming_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(2, '&Seeming', seeming_select)
            self.setTabOrder(self.characterName, seeming_select)

            kith_select = QtWidgets.QComboBox(self)
            new_vbox_height_offset += new_row(3, '&Kith', kith_select)
            self.setTabOrder(seeming_select, kith_select)

            courtInput = QtWidgets.QLineEdit(self)
            new_vbox_height_offset += new_row(4, '&Court', courtInput)
            self.setTabOrder(kith_select, courtInput)
            self.setTabOrder(courtInput, self.groupName)

            def update_kiths(_=0):
                """Update the kith options from the selected seeming"""
                kith_select.clear()
                kith_select.addItems(seeming_select.currentData())

            seeming_select.currentIndexChanged.connect(update_kiths)
            seeming_select.currentTextChanged.connect(lambda text: self.set_value('seeming', text))
            kith_select.currentTextChanged.connect(lambda text: self.set_value('kith', text))
            courtInput.textChanged.connect(lambda text: self.set_value("court", text))

            for seeming in self.prefs.get('changeling.seemings'):
                seeming_select.addItem(seeming.title(), userData=[kith.title() for kith in self.prefs.get('changeling.kiths.{}'.format(seeming))])

            self.set_value("command", commands.create_character.changeling)
            self.set_value("serialize", ['name', 'seeming', 'kith'])

        else:
            self.set_value("command", commands.create_character.standard)
            self.set_value("serialize", ['name', 'ctype'])
            self.setTabOrder(self.characterName, self.groupName)

        new_vbox_height_offset += len(self.type_specific_widgets)*6

        self.resize(
            self.width(),
            self.height() - self.current_vbox_height_offset + new_vbox_height_offset)
        self.current_vbox_height_offset = new_vbox_height_offset

    def run(self):
        """
        Show the dialog

        Returns:
            True if the OK button was pressed, False if not. Use the values
            variable to retrieve the user's inputs.
        """
        self.characterName.setFocus()
        result = self.exec_()
        return result == self.Accepted and self.values['name']
