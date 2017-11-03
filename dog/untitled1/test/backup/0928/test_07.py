# coding=utf-8
import sys
import os
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
import pymel.core as pm
import maya.cmds as cmds


class ThumbListWidget(QtWidgets.QListWidget):
    signal_layer_name = QtCore.Signal(str)
    _rows_to_del = []

    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        # self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # self.setAcceptDrops(True)
        self._dropping = False
        self.setSelectionRectVisible(True)
    # def mousePressEvent(self, event):
    #     # if event.button()==Qt.LeftButton:
    #     # self.m_drag=True
    #     # self.m_DragPosition=event.globalPos()-self.pos()
    #     # event.accept()
    #     # self.setCursor(QCursor(Qt.OpenHandCursor))
    #     if event.button() == QtCore.Qt.RightButton:
    #         print 2,'RightButton'
    #         menu = QtWidgets.QMenu(self)
    #         menu.addAction("&Del layer", self.setDelAction)
    #         menu.addAction("&Del layer and objs", self.setDelAllAction)
    #         if menu.exec_(QtGui.QCursor.pos()):
    #             print 1, 'RightButton<<<'
    #     # if event.button() == QtCore.Qt.LeftButton:
    #     #     print 1

    def keyPressEvent(self, event):
        pm.undoInfo(openChunk=True)
        if event.key() == QtCore.Qt.Key_Space:
            if self.selectedItems():
                for item in self.selectedItems():
                    layer_name = item.text()
                    layer_name = unicode(layer_name)
                    self.emit_my_signal(layer_name)
                    objs_in_layer = cmds.editDisplayLayerMembers(layer_name, query=True)
            self.reset()
        # 删除功能
        elif event.key() == QtCore.Qt.Key_Delete:
            menu = QtWidgets.QMenu(self)
            menu.addAction("&Del layer", self.setDelAction)
            menu.addAction("&Del layer and objs", self.setDelAllAction)
            if menu.exec_(QtGui.QCursor.pos()):
                print 'Key_Delete'

    def setDelAction(self):
        pm.undoInfo(openChunk=True)
        for item in self.selectedItems():
            layer_name = item.text()
            layer_name = unicode(layer_name)
            pm.delete(layer_name)
            self.takeItem(self.row(item))
        pm.undoInfo(closeChunk=True)

    def setDelAllAction(self):
        pm.undoInfo(openChunk=True)
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
        # self.signal_layer_name = layer_name
        # self.emit(self.signal_layer_name, QtCore.Signal())
        self.signal_layer_name.emit(layer_name)


class Dialog_01(QtWidgets.QMainWindow):
    def __init__(self):
        # super(QtWidgets.QMainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)

        self.setMaximumWidth(500)
        self.setMaximumHeight(900)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.listItems = {}
        myQWidget = QtWidgets.QWidget()
        myVboxlayout = QtWidgets.QVBoxLayout()
        myBoxLayout = QtWidgets.QHBoxLayout()
        myVboxlayout.addLayout(myBoxLayout)
        myQWidget.setLayout(myVboxlayout)
        self.setCentralWidget(myQWidget)
        self.listWidgetA = ThumbListWidget(self)
        display_layers = pm.ls(type='displayLayer')
        for i in display_layers:
            layer_name = i.name()
            if not ('defaultLayer' in layer_name):
                QtWidgets.QListWidgetItem(layer_name, self.listWidgetA)
        # all_items = self.listWidgetA.findItems(QString('*'), Qt.MatchWrap | Qt.MatchWildcard)
        # for item in all_items:
        #     item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        myBoxLayout.addWidget(self.listWidgetA)
        self.listWidgetB = QtWidgets.QListView(self)

        self.tar_model = QtGui.QStandardItemModel()
        self.listWidgetB.setModel(self.tar_model)
        # self.listWidgetA.my_space_signal.connect(self.update_listWidgetB)
        # self.connect(self.listWidgetA, QtCore.SIGNAL("my_space_signal"), self.update_listWidgetB)
        self.listWidgetA.setAcceptDrops(False)
        myBoxLayout.addWidget(self.listWidgetB)

        myButton = QtWidgets.QPushButton('about')
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
            self.tar_model.appendRow(QtWidgets.QStandardItem(obj))

    def slotAbout(self):
        path = os.path.dirname(__file__) + '/Q_Display_Layer_Manager.txt'
        f = open(path, 'r')
        data = f.read()
        QtWidgets.QMessageBox.about(self, "About", data.decode("utf-8"))
        f.close()


dialog_1 = Dialog_01()
dialog_1.show()

