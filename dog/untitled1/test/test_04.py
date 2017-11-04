# -*- coding: utf-8 -*-
# title       : 切换反斜杠
# description : ''
# author      : MengWei
# date        : 
# version     :
# usage       :
# notes       :

import os
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore


class Path_Change(QtWidgets.QDialog):
    def __init__(self):
        super(Path_Change, self).__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.my_lin = QtWidgets.QLineEdit()
        my_btn = QtWidgets.QPushButton()
        layout.addWidget(self.my_lin)
        layout.addWidget(my_btn)

        my_btn.clicked.connect(self.do_it)

    def do_it(self):
        path = self.my_lin.text()
        print path
        path = os.path.normpath(path)
        print path
        os.system("start explorer %s" % path)
        print path.replace('\\', '/')


if __name__ == "__main__":
    # app = QtGui.QApplication(sys.argv)
    dog = Path_Change()
    dog.show()
    # app.exec_()
