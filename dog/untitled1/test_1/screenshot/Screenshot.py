# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Screenshot.ui'
#
# Created: Mon Mar 30 11:41:46 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ScrShot(object):
    def setupUi(self, ScrShot):
        ScrShot.setObjectName(_fromUtf8("ScrShot"))
        ScrShot.resize(270, 270)
        self.verticalLayout = QtGui.QVBoxLayout(ScrShot)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelShow = QtGui.QLabel(ScrShot)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelShow.sizePolicy().hasHeightForWidth())
        self.labelShow.setSizePolicy(sizePolicy)
        self.labelShow.setText(_fromUtf8(""))
        self.labelShow.setObjectName(_fromUtf8("labelShow"))
        self.verticalLayout.addWidget(self.labelShow)
        self.groupBox = QtGui.QGroupBox(ScrShot)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelSpinBox = QtGui.QLabel(self.groupBox)
        self.labelSpinBox.setObjectName(_fromUtf8("labelSpinBox"))
        self.horizontalLayout_2.addWidget(self.labelSpinBox)
        self.spinBox = QtGui.QSpinBox(self.groupBox)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.checkBoxHideThis = QtGui.QCheckBox(self.groupBox)
        self.checkBoxHideThis.setObjectName(_fromUtf8("checkBoxHideThis"))
        self.verticalLayout_2.addWidget(self.checkBoxHideThis)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonNew = QtGui.QPushButton(ScrShot)
        self.pushButtonNew.setObjectName(_fromUtf8("pushButtonNew"))
        self.horizontalLayout.addWidget(self.pushButtonNew)
        self.pushButtonSave = QtGui.QPushButton(ScrShot)
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.pushButton_Quit = QtGui.QPushButton(ScrShot)
        self.pushButton_Quit.setObjectName(_fromUtf8("pushButton_Quit"))
        self.horizontalLayout.addWidget(self.pushButton_Quit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ScrShot)
        QtCore.QMetaObject.connectSlotsByName(ScrShot)

    def retranslateUi(self, ScrShot):
        ScrShot.setWindowTitle(_translate("ScrShot", "Form", None))
        self.groupBox.setTitle(_translate("ScrShot", "Options", None))
        self.labelSpinBox.setText(_translate("ScrShot", "Screenstot Delay:", None))
        self.checkBoxHideThis.setText(_translate("ScrShot", "Hide This Window", None))
        self.pushButtonNew.setText(_translate("ScrShot", "新建", None))
        self.pushButtonSave.setText(_translate("ScrShot", "保存", None))
        self.pushButton_Quit.setText(_translate("ScrShot", "退出", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ScrShot = QtGui.QWidget()
    ui = Ui_ScrShot()
    ui.setupUi(ScrShot)
    ScrShot.show()
    sys.exit(app.exec_())