from PySide import QtGui
from PySide import QtCore
from pymel.core import *
import os
print os.path.dirname(__file__)
print '*'*100


class resetSelCTL(QtGui.QDialog):
    def __init__(self):
        super(resetSelCTL, self).__init__()

        self.setWindowTitle('resetSelCTL')
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1200, 50, 250, 150)
        self.setModal(False)

        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))

        main_layout = QtGui.QVBoxLayout(self)

        self.button_a = QtGui.QPushButton('ResetSelCTL')
        self.button_a.setMinimumHeight(60)
        self.button_b = QtGui.QPushButton('Gtocenter')
        self.button_b.setMinimumHeight(60)
        self.button_c = QtGui.QPushButton('Change Two Value')
        self.button_c.setMinimumHeight(60)

        main_layout.addWidget(self.button_a)
        main_layout.addWidget(self.button_b)
        main_layout.addWidget(self.button_c)

        self.button_a.clicked.connect(self.resetSel)
        self.button_b.clicked.connect(self.gotocenter)
        self.button_c.clicked.connect(self.change_val)

        self.about_button = QtGui.QPushButton('about')
        main_layout.addWidget(self.about_button)

        self.about_button.clicked.connect(self.slotAbout)


    def resetSel(self):
        undoInfo(openChunk=True)
        ctrl_list = selected()
        for ctrl in ctrl_list:
            attrs = listAttr(ctrl, k=True, w=True, unlocked=True, s=True)
            for attribute in attrs:
				try:
					connections = listConnections("%s.%s" % (ctrl, attribute), s=True, d=False, scn=True)
					animated = ls(connections, type=["animCurveTT", "animCurveTA", "animCurveTL", "animCurveTU"])
					if not connections or (connections):
						values = attributeQuery(attribute, listDefault=True, n=ctrl)
						setAttr("%s.%s" % (ctrl, attribute), values[0])
				except:
					pass

        undoInfo(closeChunk=True)

    def gotocenter(self):
        obj = selected()[0]
        move(obj, (0, 0, 0), rpr=1)

    def change_val(self):
        undoInfo(openChunk=True)
        data_from = selected()[0]
        vector_m = [data_from.rx.get(), data_from.ry.get(), data_from.rz.get()]

        data_to = selected()[1]
        data_to.rx.set(-vector_m[0])
        data_to.ry.set(-vector_m[1])
        data_to.rz.set(-vector_m[2])
        undoInfo(closeChunk=True)

    def slotAbout(self):
        path = os.path.dirname(__file__) + '/about_resetSelCTL.txt'
        f = open(path, 'r')
        data = f.read()

        QtGui.QMessageBox.about(self, "About", data.decode("utf-8"))
        f.close()

        # self.label.setText("About MessageBox")

resetSelCTL = resetSelCTL()
resetSelCTL.show()