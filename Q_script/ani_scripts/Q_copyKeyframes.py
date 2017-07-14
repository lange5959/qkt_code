import maya.cmds as cmds
# import random
import sys
import os
from PySide import QtCore
from PySide import QtGui

sys.path.append(r"C:/cgteamwork/python/Lib/site-packages")
sys.path.append(r"C:/cgteamwork/bin/base")
from cgtw import *
from tw_sys import *
print os.path.dirname(__file__)

my_reference_win=""

class CopyKeyframesUI(QtGui.QDialog):
    def __init__(self):
        super(CopyKeyframesUI, self).__init__()

        self.setWindowTitle('copyKeyframes')
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1200, 50, 250, 150)
        self.setModal(False)

        #style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
       # style_sheet_file.open(QtCore.QFile.ReadOnly)
       # self.setStyleSheet(str(style_sheet_file.readAll()))

        main_layout = QtGui.QVBoxLayout(self)

        copy_key_button = QtGui.QPushButton('CopyKeyframes')
        copy_key_button.setMinimumHeight(100)
        main_layout.addWidget(copy_key_button)

        self.label = QtGui.QLabel("About Qt MessageBox")
        about_button = QtGui.QPushButton('About')
        main_layout.addWidget(about_button)

        copy_key_button.clicked.connect(self.copyKeyframes)
        about_button.clicked.connect(self.slotAbout)

    def getAttName(self, fullname):
        parts = fullname.split('.')
        return parts[-1]

    def copyKeyframes(self):
        undoInfo(closeChunk=True)


        objs = cmds.ls(selection=True)
        if (len(objs) < 2):
            cmds.error("Please select at least two objects")
        sourceObj = objs[0]
        animAttributes = cmds.listAnimatable(sourceObj);
        for attribute in animAttributes:
            numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)
            if (numKeyframes > 0):
                cmds.copyKey(attribute)
                for obj in objs[1:]:
                    cmds.pasteKey(obj, attribute=self.getAttName(attribute), option="replace")
        undoInfo(closeChunk=True)


    def slotAbout(self):
        path = os.path.dirname(__file__) + '/Q_copyKeyframes.txt'
        f = open(path, 'r')
        data = f.read()

        QtGui.QMessageBox.about(self, "About", data.decode("utf-8"))
        f.close()
        self.label.setText("About MessageBox")
# copyKeyframes()


def create_module(t_plugin_id):
    global my_reference_win
    my_reference_win=CopyKeyframesUI()
    my_reference_win.show()

