# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'npc/gui/uis/about.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setWindowModality(QtCore.Qt.WindowModal)
        AboutDialog.resize(271, 175)
        AboutDialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        AboutDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 140, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.labelProgName = QtWidgets.QLabel(AboutDialog)
        self.labelProgName.setGeometry(QtCore.QRect(0, 0, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.labelProgName.setFont(font)
        self.labelProgName.setTextFormat(QtCore.Qt.PlainText)
        self.labelProgName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProgName.setObjectName("labelProgName")
        self.labelHelpText = QtWidgets.QLabel(AboutDialog)
        self.labelHelpText.setGeometry(QtCore.QRect(10, 60, 251, 81))
        self.labelHelpText.setObjectName("labelHelpText")
        self.labelVersion = QtWidgets.QLabel(AboutDialog)
        self.labelVersion.setGeometry(QtCore.QRect(10, 30, 121, 18))
        self.labelVersion.setObjectName("labelVersion")

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About NPC"))
        self.labelProgName.setText(_translate("AboutDialog", "NPC"))
        self.labelHelpText.setText(_translate("AboutDialog", "GM helper script to manage game files.\n"
"\n"
"Copyright (c) 2015-2017 Peter Andrews\n"
"Distributed under the MIT license"))
        self.labelVersion.setText(_translate("AboutDialog", "Version"))

