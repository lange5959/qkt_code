
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import *
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtSlot, pyqtSignal
# from win32 import win32api
# import win32con
# import win32gui


def getThisColor(v, img):
    points = tuple(eval_r(v))
    rgb = img.toImage().pixel(points[0], points[1])
    red10 = QtGui.qRed(rgb)
    green10 = QtGui.qGreen(rgb)
    blue10 = QtGui.qBlue(rgb)
    color10 = "(" + str(red10) + "," + str(green10) + "," + str(blue10) + ")"
    red16 = str(hex(red10))[2:]
    green16 = str(hex(green10))[2:]
    blue16 = str(hex(blue10))[2:]
    color16 = red16 + green16 + blue16
    return color10 + "|" + color16