# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'npc/gui/uis/new_character.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewCharacterDialog(object):
    def setupUi(self, NewCharacterDialog):
        NewCharacterDialog.setObjectName("NewCharacterDialog")
        NewCharacterDialog.resize(450, 432)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewCharacterDialog.sizePolicy().hasHeightForWidth())
        NewCharacterDialog.setSizePolicy(sizePolicy)
        NewCharacterDialog.setMinimumSize(QtCore.QSize(450, 382))
        NewCharacterDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewCharacterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoForm = QtWidgets.QFormLayout()
        self.infoForm.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.infoForm.setObjectName("infoForm")
        self.typeLabel = QtWidgets.QLabel(NewCharacterDialog)
        self.typeLabel.setObjectName("typeLabel")
        self.infoForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.typeLabel)
        self.typeSelect = QtWidgets.QComboBox(NewCharacterDialog)
        self.typeSelect.setObjectName("typeSelect")
        self.infoForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.typeSelect)
        self.nameLine = QtWidgets.QLabel(NewCharacterDialog)
        self.nameLine.setObjectName("nameLine")
        self.infoForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nameLine)
        self.characterName = QtWidgets.QLineEdit(NewCharacterDialog)
        self.characterName.setObjectName("characterName")
        self.infoForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.characterName)
        self.groupLabel = QtWidgets.QLabel(NewCharacterDialog)
        self.groupLabel.setObjectName("groupLabel")
        self.infoForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.groupLabel)
        self.groupName = QtWidgets.QLineEdit(NewCharacterDialog)
        self.groupName.setObjectName("groupName")
        self.infoForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.groupName)
        self.locLabel = QtWidgets.QLabel(NewCharacterDialog)
        self.locLabel.setObjectName("locLabel")
        self.infoForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.locLabel)
        self.locName = QtWidgets.QLineEdit(NewCharacterDialog)
        self.locName.setObjectName("locName")
        self.infoForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.locName)
        self.verticalLayout.addLayout(self.infoForm)
        self.foreignBox = QtWidgets.QGroupBox(NewCharacterDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.foreignBox.sizePolicy().hasHeightForWidth())
        self.foreignBox.setSizePolicy(sizePolicy)
        self.foreignBox.setMinimumSize(QtCore.QSize(0, 71))
        self.foreignBox.setCheckable(True)
        self.foreignBox.setChecked(False)
        self.foreignBox.setObjectName("foreignBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.foreignBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.foreignText = QtWidgets.QLineEdit(self.foreignBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.foreignText.sizePolicy().hasHeightForWidth())
        self.foreignText.setSizePolicy(sizePolicy)
        self.foreignText.setClearButtonEnabled(True)
        self.foreignText.setObjectName("foreignText")
        self.verticalLayout_2.addWidget(self.foreignText)
        self.verticalLayout.addWidget(self.foreignBox)
        self.deceasedBox = QtWidgets.QGroupBox(NewCharacterDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deceasedBox.sizePolicy().hasHeightForWidth())
        self.deceasedBox.setSizePolicy(sizePolicy)
        self.deceasedBox.setMinimumSize(QtCore.QSize(0, 116))
        self.deceasedBox.setCheckable(True)
        self.deceasedBox.setChecked(False)
        self.deceasedBox.setObjectName("deceasedBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.deceasedBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.deceasedText = QtWidgets.QPlainTextEdit(self.deceasedBox)
        self.deceasedText.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.deceasedText.setObjectName("deceasedText")
        self.verticalLayout_3.addWidget(self.deceasedText)
        self.verticalLayout.addWidget(self.deceasedBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewCharacterDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.typeLabel.setBuddy(self.typeSelect)
        self.nameLine.setBuddy(self.characterName)
        self.groupLabel.setBuddy(self.groupName)

        self.retranslateUi(NewCharacterDialog)
        self.buttonBox.accepted.connect(NewCharacterDialog.accept)
        self.buttonBox.rejected.connect(NewCharacterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewCharacterDialog)
        NewCharacterDialog.setTabOrder(self.typeSelect, self.characterName)
        NewCharacterDialog.setTabOrder(self.characterName, self.groupName)
        NewCharacterDialog.setTabOrder(self.groupName, self.locName)
        NewCharacterDialog.setTabOrder(self.locName, self.foreignBox)
        NewCharacterDialog.setTabOrder(self.foreignBox, self.foreignText)
        NewCharacterDialog.setTabOrder(self.foreignText, self.deceasedBox)
        NewCharacterDialog.setTabOrder(self.deceasedBox, self.deceasedText)

    def retranslateUi(self, NewCharacterDialog):
        _translate = QtCore.QCoreApplication.translate
        NewCharacterDialog.setWindowTitle(_translate("NewCharacterDialog", "New Character"))
        self.typeLabel.setText(_translate("NewCharacterDialog", "T&ype"))
        self.typeSelect.setToolTip(_translate("NewCharacterDialog", "Type of character. Determines which fields are available."))
        self.nameLine.setText(_translate("NewCharacterDialog", "&Name"))
        self.characterName.setToolTip(_translate("NewCharacterDialog", "The character\'s name. Use \' - \' to add a brief note."))
        self.groupLabel.setText(_translate("NewCharacterDialog", "&Group"))
        self.groupName.setToolTip(_translate("NewCharacterDialog", "Main group that the character belongs to"))
        self.locLabel.setText(_translate("NewCharacterDialog", "Location"))
        self.locName.setToolTip(_translate("NewCharacterDialog", "Place where the character lives within the main setting"))
        self.foreignBox.setTitle(_translate("NewCharacterDialog", "Fore&ign"))
        self.foreignText.setPlaceholderText(_translate("NewCharacterDialog", "Where do they live?"))
        self.deceasedBox.setTitle(_translate("NewCharacterDialog", "&Deceased"))
        self.deceasedText.setPlaceholderText(_translate("NewCharacterDialog", "How did they die?"))

