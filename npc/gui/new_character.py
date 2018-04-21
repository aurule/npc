"""New character dialog"""

from PyQt5 import QtCore, QtGui, QtWidgets
from os import path

from . import commands, util
from npc.character import Character
from npc.commands.util import create_path_from_character
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
            "command": commands.create_standard,
            "name": "",
            "ctype": "",
            "dead": False,
            "foreign": False,
            "location": "",
            "groups": [],
        }

        self.setupUi(self)

        self.path_dislpay = QtWidgets.QLabel(self)
        self.infoForm.insertRow(5, 'Path:', self.path_dislpay)
        self.path_timer = QtCore.QTimer()
        self.path_timer.setSingleShot(True)
        self.path_timer.setInterval(300)
        self.path_timer.timeout.connect(self.update_path)

        self.typeSelect.currentTextChanged.connect(lambda text: self.set_value("ctype", text))
        self.characterName.textChanged.connect(lambda text: self.set_value("name", text))
        self.groupName.textChanged.connect(lambda text: self.set_value("groups", [text]))
        self.foreignBox.toggled.connect(self.set_foreign)
        self.foreignText.textChanged.connect(self.set_foreign)
        self.deceasedBox.toggled.connect(self.set_deceased)
        self.deceasedText.textChanged.connect(self.set_deceased)
        self.locName.textChanged.connect(lambda text: self.set_value("location", text))

        self._setup_type_select()

    def _setup_type_select(self):
        """
        Populate type selector and set default state
        """
        for type_key in sorted(self.prefs.get_available_types()):
            item = self.typeSelect.addItem(type_key.title(), userData=type_key)
        default_index = self.typeSelect.findText(self.prefs.get('gui.defaults.character_type').title())
        if default_index != -1:
            self.typeSelect.setCurrentIndex(default_index)
            self.update_type_specific_controls(default_index)
        self.typeSelect.currentIndexChanged.connect(self.update_type_specific_controls)

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
        self.path_timer.start()

    def update_path(self):
        """Update the path label based on current values"""

        values = self.values.copy()

        tags = {}
        tags['type'] = values['ctype']
        if values['groups']:
            tags['group'] = values.pop('groups')

        tags.update({k: v for (k, v) in values.items() if v})

        temp_char = Character()
        temp_char.merge_all({**self.prefs.get('tag_defaults'), **tags})

        template_path = self.prefs.get('types.{}.sheet_template'.format(temp_char.type_key))
        char_name = values['name']
        if char_name:
            filename = char_name + path.splitext(template_path)[1]
        else:
            filename = ''
        base_path = create_path_from_character(temp_char, prefs=self.prefs)
        final_path = path.join(base_path, filename)

        path_exists = path.exists(final_path)

        if path_exists:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

        if path_exists and char_name:
            self.path_dislpay.setText("Character already exists")
        else:
            self.path_dislpay.setText(final_path)

    def set_foreign(self, _):
        """Special handling for the compound `foreign` value"""

        if self.foreignBox.isChecked():
            if self.foreignText.text():
                self.set_value("foreign", self.foreignText.text())
            else:
                self.set_value("foreign", True)
        else:
            self.set_value("foreign", False)

    def set_deceased(self, _=None):
        """Special handling for the compound `deceased` value"""

        if self.deceasedBox.isChecked():
            if self.deceasedText.toPlainText():
                self.set_value("dead", self.deceasedText.toPlainText())
            else:
                self.set_value("dead", True)
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

        new_vbox_height_offset = 0
        type_key = self.typeSelect.itemData(index)
        if type_key == 'changeling':
            new_vbox_height_offset = self.create_changeling_controls()
        elif type_key == 'werewolf':
            new_vbox_height_offset = self.create_werewolf_controls()
        else:
            self.create_basic_controls()

        new_vbox_height_offset += len(self.type_specific_widgets)*6

        self.resize(
            self.width(),
            self.height() - self.current_vbox_height_offset + new_vbox_height_offset)
        self.current_vbox_height_offset = new_vbox_height_offset


    def new_row(self, index, title, widget):
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

    def create_basic_controls(self):
        """
        Set up the base controls

        This just means resetting the tab order and internal data structures.

        All create_*_controls methods should return the height of their controls.

        Returns:
            Zero, since this doesn't create anything
        """
        self.set_value("command", commands.create_standard)
        self.setTabOrder(self.characterName, self.groupName)
        return 0

    def create_changeling_controls(self):
        """
        Set up the changeling-specific controls

        Adds the seeming, kith, and court rows
        """
        new_vbox_height_offset = 0
        seeming_select = QtWidgets.QComboBox(self)
        new_vbox_height_offset += self.new_row(2, '&Seeming', seeming_select)
        self.setTabOrder(self.characterName, seeming_select)

        kith_select = QtWidgets.QComboBox(self)
        new_vbox_height_offset += self.new_row(3, '&Kith', kith_select)
        self.setTabOrder(seeming_select, kith_select)

        courtInput = QtWidgets.QLineEdit(self)
        new_vbox_height_offset += self.new_row(4, '&Court', courtInput)
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

        self.set_value("command", commands.create_changeling)

        return new_vbox_height_offset

    def create_werewolf_controls(self):
        """
        Set up the werewolf-specific controls

        Adds the auspice and tribe rows
        """
        new_vbox_height_offset = 0

        auspice_select = QtWidgets.QComboBox(self)
        new_vbox_height_offset += self.new_row(2, '&Auspice', auspice_select)
        for auspice in self.prefs.get('werewolf.auspices'):
            auspice_select.addItem(auspice.title())
        self.setTabOrder(self.characterName, auspice_select)

        tribe_select = QtWidgets.QComboBox(self)
        new_vbox_height_offset += self.new_row(2, '&Tribe', tribe_select)
        for tribe in self.prefs.get('werewolf.tribes.moon'):
            tribe_select.addItem(tribe.title())
        tribe_select.insertSeparator(tribe_select.count())
        for tribe in self.prefs.get('werewolf.tribes.pure'):
            tribe_select.addItem(tribe.title())
        self.setTabOrder(auspice_select, tribe_select)
        self.setTabOrder(tribe_select, self.groupName)

        auspice_select.currentTextChanged.connect(lambda text: self.set_value('auspice', text))
        tribe_select.currentTextChanged.connect(lambda text: self.set_value('tribe', text))

        return new_vbox_height_offset

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
