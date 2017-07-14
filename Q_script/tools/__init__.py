# -*- coding: utf-8 -*-
# @File : # @Author : Mengwei
# @Description : 
import sys

sys.path.append(r'C:\Python27\Lib\site-packages')
from PyQt4 import QtCore
from PyQt4 import QtGui
from Qt import QtWidgets, QtCore, QtGui


class light_tool(QtWidgets.QDialog):


    """

"""


def __init__(self):
    super(light_tool, self).__init__()

    layout = QtWidgets.QHBoxLayout(self)
    self.my_com = QtWidgets.QComboBox()
    layout.addWidget(self.my_com)

    self.my_com.addItem(u'd')
    self.my_com.addItem(u'a')


if __name__ == '__main__':
    dog = light_tool()
    dog.show()

