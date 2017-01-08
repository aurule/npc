# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'npc/gui/uis/init.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InitDialog(object):
    def setupUi(self, InitDialog):
        InitDialog.setObjectName("InitDialog")
        InitDialog.setWindowModality(QtCore.Qt.WindowModal)
        InitDialog.resize(401, 441)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InitDialog.sizePolicy().hasHeightForWidth())
        InitDialog.setSizePolicy(sizePolicy)
        InitDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(InitDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 400, 381, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(InitDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 381, 111))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.checkBoxCreateTypes = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxCreateTypes.setGeometry(QtCore.QRect(20, 70, 211, 22))
        self.checkBoxCreateTypes.setObjectName("checkBoxCreateTypes")
        self.initCampaignTitle = QtWidgets.QLineEdit(self.groupBox)
        self.initCampaignTitle.setGeometry(QtCore.QRect(120, 30, 241, 32))
        self.initCampaignTitle.setObjectName("initCampaignTitle")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 101, 31))
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(InitDialog)
        self.frame_2.setGeometry(QtCore.QRect(10, 130, 381, 261))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setObjectName("frame_2")
        self.initFoldersToCreate = QtWidgets.QTextBrowser(self.frame_2)
        self.initFoldersToCreate.setGeometry(QtCore.QRect(0, 41, 381, 211))
        self.initFoldersToCreate.setObjectName("initFoldersToCreate")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 191, 18))
        self.label_2.setObjectName("label_2")
        self.label.setBuddy(self.initCampaignTitle)

        self.retranslateUi(InitDialog)
        self.buttonBox.accepted.connect(InitDialog.accept)
        self.buttonBox.rejected.connect(InitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InitDialog)

    def retranslateUi(self, InitDialog):
        _translate = QtCore.QCoreApplication.translate
        InitDialog.setWindowTitle(_translate("InitDialog", "Campaign Setup"))
        self.groupBox.setTitle(_translate("InitDialog", "Options"))
        self.checkBoxCreateTypes.setText(_translate("InitDialog", "Create character type &folders"))
        self.initCampaignTitle.setToolTip(_translate("InitDialog", "Title for this campaign"))
        self.label.setText(_translate("InitDialog", "Campaign &Title:"))
        self.label_2.setText(_translate("InitDialog", "These folders will be created:"))

