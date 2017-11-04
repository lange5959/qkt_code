#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : QKT_UVMoverMainUI
# description : ''
# author      : MengWei
# date        : 
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging

# Third-party modules
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import pymel.core as pm

# Studio modules

# Local modules
import uv_mover

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_UVMoverMainUI_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class UVMoverMainUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UVMoverMainUI, self).__init__(parent)

        self.setFocus()
        self._ui = uv_mover.Ui_UVMover()
        self._ui.setupUi(self)
        self._history = []

    def do_move_uv(self):
        # get step
        step = 1
        # get direction
        clicked_btn = self.sender()
        btn_name = clicked_btn.objectName()
        direction_dict = {"l_up_btn": {"uValue": -step, "vValue": step},
                          "up_btn": {"vValue": step},
                          "r_up_btn": {"uValue": step, "vValue": step},
                          "left_btn": {"uValue": -step},
                          "right_btn": {"uValue": step},
                          "l_down_btn": {"uValue": -step, "vValue": -step},
                          "down_btn": {"vValue": -step},
                          "r_down_btn": {"uValue": step, "vValue": -step},
                          }
        # select uv of selection objects
        pm.mel.eval("PolySelectConvert 4")
        # do move
        pm.polyEditUVShell(**direction_dict[btn_name])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self._ui.up_btn.clicked.emit()
        if event.key() == QtCore.Qt.Key_Left:
            self._ui.left_btn.clicked.emit()
        if event.key() == QtCore.Qt.Key_Right:
            self._ui.right_btn.clicked.emit()
        if event.key() == QtCore.Qt.Key_Down:
            self._ui.down_btn.clicked.emit()


if __name__ == "__main__":
    import sys

    # app = QtGui.QApplication(sys.argv)
    wgt = UVMoverMainUI()
    wgt.show()
    # app.exec_()

PyQt4 QTextBrowser 使用教程

browser = QTextBrowser() #实例化一个textbrowser

browser.append('sdfsdfds') #追加内容

browser.setOpenLinks(True) #打开文档内部链接 默认为True

browser.setOpenExternalLinks(True) #打开外部链接 默认false 当openlinks设置false时 该选项无效

textbrowser.setSearchPaths(["ldks",":/sdfs"]) #设置文档搜索路径 参数为包含目录的List

textbrowser.setSource("index.html") #设置文档

dt=textbrowser.documentTitle() #返回文档的标题

self.connect(textbrowser,SIGNAL("SourceChanged(QUrl)"),self.update) #发出一个SourceChanged(QUrl)信号

textbrowser同时 具有以下插槽: home() :返回主文档, backward() #返回上一文档,forward()前进

browser.setDocumentTitle('dsds') #设置文档标题
