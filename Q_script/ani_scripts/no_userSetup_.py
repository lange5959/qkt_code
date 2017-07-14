# coding=utf8
# from Qt import QtCore, QtGui, QtWidgets
#from PySide2 import QtCore
#from PySide2 import QtGui
#from PySide2 import QtWidgets

from PySide import QtCore
from PySide import QtGui

import glob
import os
import time
import re
import sys
sys.path.append(r'C:\Python27\Lib\site-packages')
from pymel.core import *
import maya.cmds as mc
import maya.utils


def pySource(filePath):
    myFile = os.path.basename(filePath)
    dir = os.path.dirname(filePath)
    fileName = os.path.splitext(myFile)[0]
    if(os.path.exists(dir)):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
        if not pathfound:
            sys.path.append(dir)
    exec('import ' +fileName) in globals()
    exec('reload(' + fileName + ' )') in globals()
    return fileName

def run():
    if (menu('qkt', ex=1)):
        deleteUI(['qkt'], menu=1)
    # Q_path = os.path.dirname(__file__)
    menu('qkt', label=u'其卡通', parent=setParent('MayaWindow'), tearOff=True)
    # Q_mayaFont_py = 'pySource(' +'\'' + Q_path + '/Q_mayaFont.py' + '\'' + ')'
    # print Q_mayaFont_py
    menuItem(label=u'菜单字体放大', c="pySource(r'Q:/rig/scripts/ani_scripts/Q_mayaFont.py')", tearOff=True)
    menuItem(label=u'打开工程文件夹', c="pySource(r'Q:/rig\scripts/ani_scripts/Q_openFolder.py')", tearOff=True)
    menuItem(label=u'另存文件', c="pySource(r'Q:/rig\scripts/ani_scripts/Q_SaveFile.py')", tearOff=True)
    menuItem(subMenu=1, label=u'动画', tearOff=1)
    menuItem(label=u'相机抖动', c="pySource(r'Q:/rig/scripts/test/ani/Q_Handheld_camera_shooting.py')")
    # Result: ui.CommandMenuItem('window1|menu49|menuItem479|menuItem480') #
    menuItem(label=u'转TPose', c="pySource(r'Q:/rig/scripts/ani_scripts/Q_resetSelCTL.py')")
    # Result: ui.CommandMenuItem('window1|menu49|menuItem479|menuItem481') #
    menuItem(label='ddd')
    setParent('..', menu=True)

    menuItem(label='File', tearOff=True)
    menuItem(divider=True)

    menuItem(subMenu=1, label=u'常用工具', tearOff=1)
    menuItem(label=u'序列改名', c="pySource(r'Q:/rig/scripts/ani_scripts/Q_rename.py')")
    # Result: ui.CommandMenuItem('window1|menu49|menuItem479|menuItem480') #
    menuItem(label='Green')
    # Result: ui.CommandMenuItem('window1|menu49|menuItem479|menuItem481') #
    menuItem(label='Yellow')
    setParent('..', menu=True)

maya.utils.executeDeferred(run)