# -*- coding: utf-8 -*-
# title       :
# description : ''
# author      : MengWei
# date        :
# version     :
# usage       :
# notes       :

import sys
from PyQt4 import QtGui, QtCore

import os, string
import math

THUMB_WIDTH = 128
THUMB_HEIGHT = 128
THUMB_MIN = 64
THUMB_MAX = 256

FILE_TYPE = ['jpg', 'jpeg']


class ImageWidget(QtGui.QWidget):
    prevSelected = None

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.id = 0
        self.displayText = ''
        self.version = ''
        self.status = 0
        self.path = ''
        self.showStatus = True
        self.selected = False
        self.isHightlight = False
        self.thumb = QtGui.QImage()
        self.initAttrib()

    def initAttrib(self):
        self.name_font = QtGui.QFont()
        self.bg_color = QtGui.QColor(50, 50, 50)
        self.hightlight = QtGui.QColor(255, 255, 255, 100)
        self.edge_size = 5
        self.pen_selected = QtGui.QPen(QtGui.QColor(255, 255, 0))
        self.


