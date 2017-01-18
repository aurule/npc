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
        NewCharacterDialog.resize(412, 750)
        NewCharacterDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewCharacterDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 700, 371, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(NewCharacterDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 41, 31))
        self.label.setObjectName("label")
        self.typeSelect = QtWidgets.QComboBox(NewCharacterDialog)
        self.typeSelect.setGeometry(QtCore.QRect(60, 20, 321, 32))
        self.typeSelect.setEditable(True)
        self.typeSelect.setObjectName("typeSelect")
        self.label_2 = QtWidgets.QLabel(NewCharacterDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 51, 31))
        self.label_2.setObjectName("label_2")
        self.characterName = QtWidgets.QLineEdit(NewCharacterDialog)
        self.characterName.setGeometry(QtCore.QRect(60, 60, 321, 32))
        self.characterName.setObjectName("characterName")
        self.deceasedBox = QtWidgets.QGroupBox(NewCharacterDialog)
        self.deceasedBox.setGeometry(QtCore.QRect(60, 510, 321, 101))
        self.deceasedBox.setCheckable(True)
        self.deceasedBox.setChecked(False)
        self.deceasedBox.setObjectName("deceasedBox")
        self.deceasedText = QtWidgets.QPlainTextEdit(self.deceasedBox)
        self.deceasedText.setGeometry(QtCore.QRect(10, 30, 301, 61))
        self.deceasedText.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.deceasedText.setObjectName("deceasedText")
        self.foreignBox = QtWidgets.QGroupBox(NewCharacterDialog)
        self.foreignBox.setGeometry(QtCore.QRect(60, 430, 321, 71))
        self.foreignBox.setCheckable(True)
        self.foreignBox.setChecked(False)
        self.foreignBox.setObjectName("foreignBox")
        self.foreignText = QtWidgets.QLineEdit(self.foreignBox)
        self.foreignText.setGeometry(QtCore.QRect(10, 30, 301, 32))
        self.foreignText.setClearButtonEnabled(True)
        self.foreignText.setObjectName("foreignText")
        self.groupsBox = QtWidgets.QGroupBox(NewCharacterDialog)
        self.groupsBox.setGeometry(QtCore.QRect(60, 100, 321, 321))
        self.groupsBox.setObjectName("groupsBox")
        self.label.setBuddy(self.typeSelect)
        self.label_2.setBuddy(self.characterName)

        self.retranslateUi(NewCharacterDialog)
        self.buttonBox.accepted.connect(NewCharacterDialog.accept)
        self.buttonBox.rejected.connect(NewCharacterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewCharacterDialog)

    def retranslateUi(self, NewCharacterDialog):
        _translate = QtCore.QCoreApplication.translate
        NewCharacterDialog.setWindowTitle(_translate("NewCharacterDialog", "New Character"))
        self.label.setText(_translate("NewCharacterDialog", "&Type:"))
        self.label_2.setText(_translate("NewCharacterDialog", "&Name"))
        self.deceasedBox.setTitle(_translate("NewCharacterDialog", "&Deceased"))
        self.deceasedText.setPlaceholderText(_translate("NewCharacterDialog", "How did they die?"))
        self.foreignBox.setTitle(_translate("NewCharacterDialog", "&Foreign"))
        self.foreignText.setPlaceholderText(_translate("NewCharacterDialog", "Where do they live?"))
        self.groupsBox.setTitle(_translate("NewCharacterDialog", "Groups"))

