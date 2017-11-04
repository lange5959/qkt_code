# coding=utf-8
# 数据库测试，聂佳利，树形图显示
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import requests, json


class MyTreeView(QTreeWidget):

    def __init__(self):
        super(MyTreeView, self).__init__()
        super(QTreeView, self).__init__()
        self.clicked.connect(self.on_treeview_clicked2)
        # Context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)


    def on_treeview_clicked2(self):
        print 1

    def openMenu(self, position):
        self.popup_menu = QtGui.QMenu(parent=self)
        self.popup_menu.addAction("New", self.new)
        self.popup_menu.addAction("Rename", self.new)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Copy", self.copy)
        self.popup_menu.addAction("Cut", self.cut)
        self.popup_menu.addAction("Paste", self.paste)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Delete", self.deleteItem)
        self.popup_menu.exec_(self.viewport().mapToGlobal(position))

    def new(self):
        """Unfinnished"""
        print 100
        try:
            currentIndex = self.currentIndex()
            currentItem = currentIndex.internalPointer()
            print currentItem.displayData[0]
        except:
            print 'stupid error'
        print 101

    def cut(self):
        """Cut a node"""
        self.cutIndex = self.currentIndex()
        self.copyIndex = None

    def copy(self):
        """Copy a node"""
        self.cutIndex = None
        self.copyIndex = self.currentIndex()

    def paste(self):
        """Paste a node
        A node is pasted before the selected destination node
        """

        sourceIndex = None
        if self.cutIndex != None:
            sourceIndex = self.cutIndex
        elif self.copyIndex != None:
            sourceIndex = self.copyIndex

        if sourceIndex != None:
            destinationIndex = self.currentIndex()
            destinationItem = destinationIndex.internalPointer()
            destinationParent = destinationItem.parent
            destinationParentIndex = self.myModel.parent(index=destinationIndex)
            sourceItem = sourceIndex.internalPointer()
            sourceRow = sourceItem.row()
            sourceParentIndex = self.myModel.parent(index=sourceIndex)
            row = destinationItem.row()
            if self.cutIndex != None:
                self.myModel.moveItem(sourceParentIndex=sourceParentIndex,
                                      sourceRow=sourceRow,
                                      destinationParentIndex=destinationParentIndex,
                                      destinationRow=row)
            else:
                self.myModel.copyItem(sourceParentIndex=sourceParentIndex,
                                      sourceRow=sourceRow,
                                      destinationParentIndex=destinationParentIndex,
                                      destinationRow=row)

    def deleteItem(self):
        """Deletes the current item (node)"""
        currentIndex = self.currentIndex()
        currentItem = currentIndex.internalPointer()
        quitMessage = "Are you sure that %s should be deleted?" % currentItem.displayData
        messageBox = QtGui.QMessageBox(parent=self)
        reply = messageBox.question(self, 'Message',
                                    quitMessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # This item is this row at its parents child list:
            row = currentItem.row()
            parentIndex = self.myModel.parent(index=currentIndex)
            self.myModel.removeRow(row=row, parentIndex=parentIndex)

    def get_sql(self, id=0, name=''):
        #
        search = str(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search, 'key': 1}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text

        root_name = {}
        for i in r.json():
            name_a = i['name']
            id = i['id']
            root_name[name_a] = id
            # name_a = name_a.encode('utf-8')
            # print type(name_a)
        return root_name


class TreeWidget(QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__()
        QWidget.__init__(self, parent)

        self.setWindowTitle('TreeWidget')
        # 创建一个Qtree部件
        self.tree = MyTreeView()
        # 设置部件的列数为2
        self.tree.setColumnCount(2)
        # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.tree.setHeaderLabels(['Key', 'Value'])

        root_name = self.get_sql(id=0)
        print root_name
        for k, v in root_name.items():
            print k, v
            i = 0
            root = 'root_'+str(i)
            root = QTreeWidgetItem(self.tree)
            root.setText(0, k)
            # 为root节点设置子结点
            child1 = QTreeWidgetItem(root)
            child1.setText(0, 'dog')
            child1.setText(1, 'name1')

            child1 = QTreeWidgetItem(root)
            child1.setText(0, 'dog2')
            child1.setText(1, 'name12')
            self.tree.addTopLevelItem(root)
            # 将tree部件设置为该窗口的核心框架
            self.setCentralWidget(self.tree)
            i += 1

    def get_sql(self, id=0, name=''):
        #
        search = str(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search, 'key': 1}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text

        root_name = {}
        for i in r.json():
            name_a = i['name']
            id = i['id']
            root_name[name_a] = id
            # name_a = name_a.encode('utf-8')
            # print type(name_a)
        return root_name

app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
tp = TreeWidget()
tp.show()
app.exec_()