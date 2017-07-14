from PySide import QtCore
from PySide import QtGui
import sys
import os
sys.path.append(r"C:/cgteamwork/python/Lib/site-packages")
sys.path.append(r"C:/cgteamwork/bin/base")
from cgtw import *
from tw_sys import *
print os.path.dirname(__file__)
my_reference_win=""

class Base(object):
    def __init__(self):
        super(Base, self).__init__()
        
    def enterEvent(self, event):
        # super(self.__class__, self).enterEvent(event)
        print "xxx"
        

class mytesttool(Base, QtGui.QPushButton):
    def __init__(self):
        super(mytesttool, self).__init__()
        print '12'





def create_module(t_plugin_id):
    global my_reference_win
    my_reference_win=mytesttool()
    my_reference_win.show()