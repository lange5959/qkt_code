# -*- coding: utf-8 -*-
# title       : asset
# description : ''
# author      : MengWei
# date        :
# version     :
# usage       :
# notes       :

import pymel.core as pm
import maya.OpenMayaUI as omui
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

try:
    from shiboken2 import wrapInstance
except:
    from shiboken import wrapInstance


def _get_maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(long(pointer), QtWidgets.QWidget)


class FontCus(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FontCus, self).__init__(_get_maya_main_window())
        self.setWindowTitle('Font of mayaUI')

        self.font_combbox = QtWidgets.QComboBox()
        fonts = [u"monaco", 'Microsoft YaHei', 'Arial', 'Tahoma', 'Segoe UI']
        for i in fonts:
            self.font_combbox.addItem(i)

        self.fontBox = QtWidgets.QFontComboBox()
        self.fontBox.setFontFilters(QtWidgets.QFontComboBox.ScalableFonts)

        self.font_size_spinbox = QtWidgets.QSpinBox()
        self.font_size_spinbox.setValue(10)

        self.bold_checkbox = QtWidgets.QCheckBox("Bold")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.font_combbox)
        main_layout.addWidget(self.font_size_spinbox)
        main_layout.addWidget(self.fontBox)
        # main_layout.addWidget(self.bold_checkbox)

        orig_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(orig_layout)
        orig_layout.addWidget(self.bold_checkbox)

        self.orig_button2017 = QtWidgets.QPushButton(u"恢复默认(2017)")
        self.orig_button2015 = QtWidgets.QPushButton(u"恢复默认(2015)")
        orig_layout.addWidget(self.orig_button2017)
        orig_layout.addWidget(self.orig_button2015)

        self.font_combbox.currentIndexChanged.connect(self.set_font)
        self.font_size_spinbox.valueChanged.connect(self.set_font)
        self.fontBox.activated.connect(self.slotFont)
        self.bold_checkbox.stateChanged.connect(self.setBold)
        self.orig_button2017.clicked.connect(self.recovery)
        self.orig_button2015.clicked.connect(self.recovery2015)

    def set_font(self):
        font_family = self.font_combbox.currentText()
        font_size = self.font_size_spinbox.value()
        font = QtGui.QFont(font_family, font_size)
        QtWidgets.QApplication.setFont(font)

    def setBold(self):
        font_family = self.font_combbox.currentText()
        font_size = self.font_size_spinbox.value()

        # print self.bold_checkbox.checkState()
        if self.bold_checkbox.isChecked():
            font = QtGui.QFont(font_family, font_size, QtGui.QFont.Bold)
            QtWidgets.QApplication.setFont(font)
        else:
            font = QtGui.QFont(font_family, font_size)
            QtWidgets.QApplication.setFont(font)

    def slotFont(self):
        font_family = self.fontBox.currentFont().family()
        font_size = self.font_size_spinbox.value()
        font = QtGui.QFont(font_family, font_size, QtGui.QFont.Bold)
        QtWidgets.QApplication.setFont(font)

    def recovery(self):
        font = QtGui.QFont("Segoe UI", 10)
        QtWidgets.QApplication.setFont(font)
        self.font_combbox.setCurrentIndex(self.font_combbox.findText("Segoe UI"))
        self.font_size_spinbox.setValue(10)
        self.bold_checkbox.setChecked(0)

    def recovery2015(self):
        font = QtGui.QFont("Segoe UI", 10)
        QtWidgets.QApplication.setFont(font)
        self.font_combbox.setCurrentIndex(self.font_combbox.findText("Tahoma"))
        self.font_size_spinbox.setValue(10)
        self.bold_checkbox.setChecked(0)


def main():
    global win
    if "win" in globals():
        win.deleteLater()
    win = FontCus()
    win.show()

main()

if __name__ == "__main__":
    import sys

    # app = QtGui.QApplication(sys.argv)
    wgt = UVMoverMainUI()
    wgt.show()
    # app.exec_()