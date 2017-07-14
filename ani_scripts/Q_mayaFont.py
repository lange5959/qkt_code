from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 

from PySide.QtCore import * 
from PySide.QtGui import *
# vfrom PySide2.QtWidgets import *
from shiboken import wrapInstance 



omui.MQtUtil.mainWindow()  
ptr = omui.MQtUtil.mainWindow()    
widget = wrapInstance(long(ptr), QWidget)

def changeMayaBackgroundColor(color='rgb(180, 190, 170)', fontWeight='bold', font_size='12px'):

    widget.setStyleSheet(

        'font-weight:%s;'%fontWeight +
        'font-size:%s;'%font_size +
        'color:%s;'%color
        )
# 'background-color:%s;'%background +   
changeMayaBackgroundColor()

widgetStr = mel.eval( 'string $tempString = $gMainCreateMenu' )    
ptr = omui.MQtUtil.findControl( widgetStr )    
widget = wrapInstance(long(ptr), QWidget)

def changeMayaMenuColors(fontStyle='italic', fontWeight='bold', fontColor='rgb(200,200,200)', font_size='15px'):
    widget.setStyleSheet(
        'font-size:%s;'%font_size +
        'font-weight:%s;'%fontWeight +
        'color:%s;'%fontColor
        )
    # 'font-style:%s;' % fontStyle +


changeMayaMenuColors()