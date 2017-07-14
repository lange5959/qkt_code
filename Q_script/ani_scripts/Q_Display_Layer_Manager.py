# -*- coding: utf-8 -*-
__Author__ = 'Mengwei'
# @Description :
# coding=utf-8
import pymel.core as pm
import maya.cmds as cmds
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QString
import sys
sys.path.append(r'Q:\rig\scripts\Q_script\lib\Maya2016')
import os


class ThumbListWidget(QtGui.QListWidget):
    signal_layer_name = ''

    _rows_to_del = []
    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        # self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        # self.setAcceptDrops(True)
        self._dropping = False

        self.setSelectionRectVisible(True)
        # self.connect(self, QtCore.SIGNAL("dropped"), self.items_dropped)

    # def dragEnterEvent(self, event):
    #
    #     super(ThumbListWidget, self).dragEnterEvent(event)

    # def dragMoveEvent(self, event):
    #
    #     if event.mimeData().hasUrls():
    #         event.setDropAction(QtCore.Qt.CopyAction)
    #         event.accept()
    #     else:
    #         super(ThumbListWidget, self).dragMoveEvent(event)

    # def dropEvent(self, event):
    #     if event.source() is self:
    #         event.setDropAction(QtCore.Qt.MoveAction)
    #     else:
    #         event.setDropAction(QtCore.Qt.CopyAction)
    #     self._dropping = True
    #     super(ThumbListWidget, self).dropEvent(event)
    #     self._dropping = False

    # def rowsInserted(self, parent, start, end):
    #     # 不能勾选了
    #     if self._dropping:
    #         self.emit(QtCore.SIGNAL("dropped"), (start, end))
    #     super(ThumbListWidget, self).rowsInserted(parent, start, end)

    # def dataChanged(self, start, end):
    #     # 不能重复
    #     if self._dropping:
    #         for row in range(start.row(), end.row() + 1):
    #             index = self.indexFromItem(self.item(row))
    #             print self.item(row).text()
    #             shot = index.data().toString()
    #             if len(self.findItems(shot, Qt.MatchExactly)) > 1:
    #                 self._rows_to_del.append(row)
    #         self._rows_to_del.reverse()
    #         for row in self._rows_to_del:
    #             self.takeItem(row)
    #             print 0
    #         self._rows_to_del = []

    # def items_dropped(self, arg):
    #     start, end = arg
    #     for row in range(start, end + 1):
    #         item = self.item(row)
    #         item.setCheckState(Qt.Checked)

    def keyPressEvent(self, event):
        pm.undoInfo(openChunk=True)
        if event.key() == Qt.Key_Space:

            if self.selectedItems():
                for item in self.selectedItems():
                    layer_name = item.text()
                    layer_name = unicode(layer_name)
                    self.emit_my_signal(layer_name)
                    objs_in_layer = cmds.editDisplayLayerMembers(layer_name, query=True)
                    # new_state = Qt.Unchecked if item.checkState() else Qt.Checked
                    # if item.flags() & Qt.ItemIsUserCheckable:
                    #     print 1
                    #     item.setCheckState(new_state)
            self.reset()
        # 删除功能

        elif event.key() == Qt.Key_Delete:
            menu = QtGui.QMenu(self)
            menu.addAction("&Del layer", self.setDelAction)
            menu.addAction("&Del layer and objs", self.setDelAllAction)
            if menu.exec_(QtGui.QCursor.pos()):
                print 1
        #     for item in self.selectedItems():
        #         layer_name = item.text()
        #         layer_name = unicode(layer_name)
        #         objs_in_layer = cmds.editDisplayLayerMembers(layer_name, query=True)
        #         if objs_in_layer is not None:
        #             print '1'
        #             self.takeItem(self.row(item))
        #             for i in objs_in_layer:
        #                 print i
        #                 pm.delete(i)
        #             self.takeItem(self.row(item))
        #             pm.delete(layer_name)
        #         else:
        #             self.takeItem(self.row(item))
        #             pm.delete(layer_name)
        # pm.undoInfo(closeChunk = True)
    def setDelAction(self):
        # self.dropAction = Qt.CopyAction
        pm.undoInfo(openChunk=True)
        # self.dropAction = Qt.MoveAction
        for item in self.selectedItems():
            layer_name = item.text()
            layer_name = unicode(layer_name)
            pm.delete(layer_name)
            self.takeItem(self.row(item))
        pm.undoInfo(closeChunk=True)

    def setDelAllAction(self):
        pm.undoInfo(openChunk=True)
        # self.dropAction = Qt.MoveAction
        for item in self.selectedItems():
            layer_name = item.text()
            layer_name = unicode(layer_name)
            objs_in_layer = cmds.editDisplayLayerMembers(layer_name, query=True)
            if objs_in_layer is not None:
                self.takeItem(self.row(item))
                for i in objs_in_layer:
                    pm.delete(i)
                self.takeItem(self.row(item))
                pm.delete(layer_name)
            else:
                self.takeItem(self.row(item))
                pm.delete(layer_name)
        pm.undoInfo(closeChunk=True)

    def emit_my_signal(self, layer_name):
        # self.my_space_signal.emit(layer_name)
        self.signal_layer_name = layer_name
        self.emit(QtCore.SIGNAL("my_space_signal"), self.signal_layer_name)


class Dialog_01(QtGui.QMainWindow):

    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()

        self.setMaximumWidth(500)
        self.setMaximumHeight(900)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.listItems = {}
        myQWidget = QtGui.QWidget()
        myVboxlayout = QtGui.QVBoxLayout()
        myBoxLayout = QtGui.QHBoxLayout()
        myVboxlayout.addLayout(myBoxLayout)
        myQWidget.setLayout(myVboxlayout)
        self.setCentralWidget(myQWidget)
        self.listWidgetA = ThumbListWidget(self)
        display_layers = pm.ls(type='displayLayer')
        for i in display_layers:
            layer_name = i.name()
            if not ('defaultLayer' in layer_name):
                QtGui.QListWidgetItem(layer_name, self.listWidgetA)
        # all_items = self.listWidgetA.findItems(QString('*'), Qt.MatchWrap | Qt.MatchWildcard)
        # for item in all_items:
        #     item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        myBoxLayout.addWidget(self.listWidgetA)
        self.listWidgetB = QtGui.QListView(self)

        self.tar_model = QtGui.QStandardItemModel()
        self.listWidgetB.setModel(self.tar_model)
        # self.listWidgetA.my_space_signal.connect(self.update_listWidgetB)
        self.connect(self.listWidgetA, QtCore.SIGNAL("my_space_signal"), self.update_listWidgetB)
        self.listWidgetA.setAcceptDrops(False)
        myBoxLayout.addWidget(self.listWidgetB)

        myButton = QtGui.QPushButton('about')
        myButton.clicked.connect(self.slotAbout)
        myVboxlayout.addWidget(myButton)
        self.setWindowTitle('Display Layer Manager')

    def update_listWidgetB(self, layer_name):
        self.tar_model.clear()
        objs_in_layer = cmds.editDisplayLayerMembers(layer_name, query=True)
        if objs_in_layer == None:
            print 'empty layer'
            return
        print str(len(objs_in_layer)) + ' objs in ' + layer_name
        for obj in objs_in_layer:

            self.tar_model.appendRow(QtGui.QStandardItem(obj))

    def slotAbout(self):
        path = os.path.dirname(__file__) + '/Q_Display_Layer_Manager.txt'
        f = open(path, 'r')
        data = f.read()

        QtGui.QMessageBox.about(self, "About", data.decode("utf-8"))

        f.close()

# if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     dialog_1 = Dialog_01()
#     dialog_1.show()
#     dialog_1.resize(480, 320)
#     sys.exit(app.exec_())

dialog_1 = Dialog_01()
dialog_1.show()

