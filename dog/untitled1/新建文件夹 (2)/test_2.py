# coding=utf-8
"""
路径转换成反斜杠
打开文件夹


"""
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
        os.system("start explorer %s" % path)
        print path.replace('\\', '/')

dog = Path_Change()
dog.show()


