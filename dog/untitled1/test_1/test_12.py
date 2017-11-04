from PyQt4 import QtCore, QtGui
import pyc
import sys


class MyDialog(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = pyc.Ui_MainWindow()
        self.ui.setupUi(self)


def run():
    app = QtGui.QApplication(sys.argv)

    d = MyDialog()
    d.show()

    sys.exit(app.exec_())

run()