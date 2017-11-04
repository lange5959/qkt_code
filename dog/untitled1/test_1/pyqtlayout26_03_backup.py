# -*- coding: utf-8 -*-

import sys
import os
import pprint
import requests
import logging

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from maya import OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pm
import MyTimer
# QtCore.QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

projects = [u'项目', u'摇摇车', u'桂宝', u'萤火1',u'萤火2',u'神四', u'神三', u'神二', u'神一']

logging.basicConfig()
logger = logging.getLogger('lightingManager')
logger.setLevel(logging.DEBUG)

import Qt
if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal

elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal


class SplitterWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWidget, self).__init__(parent)

        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)

        leftText = QtWidgets.QTextEdit((u"左窗口<br>sldjflksjdklf"), mainSplitter)
        leftText.setAlignment(QtCore.Qt.AlignCenter)

        rightSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        upText = QtWidgets.QTextEdit((u"上窗口"), rightSplitter)
        upText.setAlignment(QtCore.Qt.AlignCenter)

        bottomText = QtWidgets.QTextEdit((u"下窗口"), rightSplitter)
        bottomText.setAlignment(QtCore.Qt.AlignCenter)

        mainSplitter.setStretchFactor(1, 20)
        rightSplitter.setStretchFactor(2, 1)
        # mainSplitter.setWindowTitle(("分割窗口"))

        self.setCentralWidget(mainSplitter)


class ThumbListWidget(QtWidgets.QListWidget):
    addfile = QtCore.Signal(str)
    # dropped = QtCore.pyqtSignal(int, int)
    dropped = QtCore.Signal(int, int)
    # dropped = QtCore.Signal(QtCore.QObject)
    _rows_to_del = []

    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.dropAction = QtCore.Qt.CopyAction
        self._dropping = False
        self.setSelectionRectVisible(True)
        self.dropped.connect(self.items_dropped)

        # self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.openMenu)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print event.mimeData().urls()
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.source() is self:
            pass
            # event.setDropAction(QtCore.Qt.MoveAction)
        else:
            event.setDropAction(QtCore.Qt.CopyAction)
        self._dropping = True
        super(ThumbListWidget, self).dropEvent(event)
        self._dropping = False
        # menu = QtWidgets.QMenu(self)
        # menu.addAction("&Copy", self.setCopyAction)
        # menu.addAction("&Move", self.setMoveAction)
        # if menu.exec_(QtGui.QCursor.pos()):
        #     # item = QListWidgetItem(text, self)
        #     # item.setIcon(icon)
        #     event.setDropAction(self.dropAction)
        #     event.accept()
        #     return
        # else:
        #     event.setDropAction(QtCore.Qt.IgnoreAction)

    def setCopyAction(self):
        print 'copy'
        # self.dropAction = Qt.CopyAction

    def setMoveAction(self):
        print 'move'
        # self.dropAction = Qt.MoveAction

    def rowsInserted(self, parent, start, end):
        if self._dropping:
            self.dropped.emit(start, end)
        super(ThumbListWidget, self).rowsInserted(parent, start, end)

    def dataChanged(self, start, end, *args, **kwargs):
        if self._dropping:
            for row in range(start.row(), end.row() + 1):
                index = self.indexFromItem(self.item(row))
                shot = index.data()
                self.addfile.emit(shot)
                if len(self.findItems(shot, QtCore.Qt.MatchExactly)) > 1:
                    self._rows_to_del.append(row)
            # self._rows_to_del.reverse()
            # for row in self._rows_to_del:
            #     self.takeItem(row)
            self._rows_to_del = []

    def items_dropped(self, start, end):
        for row in range(start, end + 1):
            item = self.item(row)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.selectedItems():
                new_state = QtCore.Qt.Unchecked if self.selectedItems()[0].checkState() else QtCore.Qt.Checked
                for item in self.selectedItems():
                    if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                        item.setCheckState(new_state)
            self.reset()
        elif event.key() == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():
                # self.takeItem(self.row(item))
                menu = QtWidgets.QMenu(self)
                menu.addAction("&Del ref", self.setDelAction)
                # menu.addAction("&000", self.setDelAllAction)
                if menu.exec_(QtGui.QCursor.pos()):
                    print 1
                # ref_name = pm.selected()[0].name()
                # cmds.referenceQuery(ref_name, isNodeReferenced=True)
                # path = cmds.referenceQuery(ref_name, filename=True)
                # topRef = cmds.referenceQuery(path, referenceNode=True, topReference=True)
                # topPath = cmds.referenceQuery(topRef, filename=True)
                # cmds.file(topPath, rr=1)

    def setDelAction(self):
        # self.dropAction = Qt.CopyAction
        pm.undoInfo(openChunk=True)
        # self.dropAction = Qt.MoveAction
        for item in self.selectedItems():
            ref_name = item.text()
            print ref_name, "<<<<<<<<<<<<<<<<<<<<<"
            layer_name = unicode(ref_name)
            # pm.delete(ref_name)
            pm.select(ref_name)
            ref_name = pm.selected()[0].name()

            cmds.referenceQuery(ref_name, isNodeReferenced=True)
            path = cmds.referenceQuery(ref_name, filename=True)
            topRef = cmds.referenceQuery(path, referenceNode=True, topReference=True)
            topPath = cmds.referenceQuery(topRef, filename=True)
            cmds.file(topPath, rr=1)
            self.takeItem(self.row(item))
        pm.undoInfo(closeChunk=True)

    # def openMenu(self, position):
    #     self.popup_menu = QtWidgets.QMenu(parent=self)
    #     self.popup_menu.addAction("New", self.new)
    #     self.popup_menu.addAction("Rename", self.new)
    #     self.popup_menu.addSeparator()
    #     self.popup_menu.addAction("Copy", self.copy)
    #     self.popup_menu.addAction("Cut", self.cut)
    #     self.popup_menu.addAction("Paste", self.paste)
    #     self.popup_menu.addSeparator()
    #     self.popup_menu.addAction("Delete", self.deleteItem)
    #     self.popup_menu.exec_(self.viewport().mapToGlobal(position))

    def new(self):
        """Unfinnished"""
        print 'list widget 001'

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


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)

        # self.library = strack_library.ControllerLibrary()
        self.sql_dict = {}

        self.buildUI()
        self.tool_list = []
        self.populate()
        self.ref_item = []
        self.ref_file = ''
        self.library_sql = {}
        self.ref_ed_obj = {}
        self.current_pid = ''

        self.setWindowTitle((u"依靠窗口"))

    def buildUI(self):

        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)

        self.tree = QtWidgets.QTreeWidget()
        # tree
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Category', 'Value'])

        root = QtWidgets.QTreeWidgetItem(self.tree)
        root.setText(0, u'模型')

        search = "1"
        inputfiled = "pid"
        sql_info = self.sql_back(search, inputfiled)

        for i in sql_info:
            print i[1]
            QtWidgets.QTreeWidgetItem(root, [i[1]], 0)
            name_test = i[1]
            print name_test, type(name_test), 'name_test<<<<<<<<<<<<<<<<<<<<'
            self.sql_dict[name_test] = i[2]
        for k, v in self.sql_dict.items():
            print k, v

        self.tree.addTopLevelItem(root)
        self.tree.clicked.connect(self.on_treeview_clicked3)

        # leftText = QtWidgets.QTextEdit((u"左窗口<br>tree"), mainSplitter)
        # leftText.setAlignment(QtCore.Qt.AlignCenter)
        mainSplitter.addWidget(self.tree)

        rightSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        self.listWidget = ThumbListWidget(self)
        self.listWidget2 = ThumbListWidget(self)

        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.listItemRightClicked)

        self.listWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget2.customContextMenuRequested.connect(self.listItemRightClicked2)

        self.listWidget2.addfile.connect(self.ref_something)

        # upText = QtWidgets.QTextEdit((u"上窗口"), rightSplitter)
        # upText.setAlignment(QtCore.Qt.AlignCenter)
        rightSplitter.addWidget(self.listWidget)
        rightSplitter.addWidget(self.listWidget2)

        # bottomText = QtWidgets.QTextEdit((u"下窗口"), rightSplitter)
        # bottomText.setAlignment(QtCore.Qt.AlignCenter)

        size = 64
        buffer = 12
        # self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        self.listWidget.setDragEnabled(True)

        # self.listWidget2.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget2.setIconSize(QtCore.QSize(size, size))
        self.listWidget2.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget2.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        self.listWidget2.setDragEnabled(True)

        mainSplitter.setStretchFactor(1, 20)
        rightSplitter.setStretchFactor(2, 1)
        # mainSplitter.setWindowTitle(("分割窗口"))

        # widget = SplitterWidget()

        self.setCentralWidget(mainSplitter)

        #停靠窗口 1
        dock1=QtWidgets.QDockWidget((u"停靠窗口 1"),self)
        dock1.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        te1=QtWidgets.QTextEdit((u"窗口 1,可在 Main Window 的左部和右部停靠，不可浮动，不可关闭"))
        dock1.setWidget(te1)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock1)

        #停靠窗口 2
        dock2=QtWidgets.QDockWidget((u"停靠窗口 2"),self)
        dock2.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetClosable)
        # dock2.setTitleBarWidget()
        te2=QtWidgets.QTextEdit((u"窗口 2,只可浮动"))
        dock2.setWidget(te2)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock2)

        #停靠窗口 2
        dock4=QtWidgets.QDockWidget((u"停靠窗口 4"),self)
        dock4.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetClosable)
        te4=QtWidgets.QTextEdit((u"窗口 4,只可浮动"))
        dock4.setWidget(te4)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock4)

        #停靠窗口 3
        dock3=QtWidgets.QDockWidget((u"停靠窗口 3"),self)
        dock3.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        te3=QtWidgets.QTextEdit((u"窗口 3,可在 Main Window 任意位置停靠，可浮动，可关闭"))
        dock3.setWidget(te3)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,dock3)

        #dock1 和dock4 合并
        self.tabifyDockWidget(dock1, dock4)

    def populate(self):
        pass
        # self.listWidget.clear()
        # path = self.lineEditFilePath.text()
        # if os.path.isdir(path):
        #     pass
        # else:
        #     path = os.path.dirname(path)
        # # print path
        # self.library.find(directory=path)
        #
        # for name, info in self.library.items():
        #     item = QtWidgets.QListWidgetItem(name)
        #     self.listWidget.addItem(item)
        #     self.tool_list.append(name)
        #
        #     screenshot = info.get('screenshot')
        #     if screenshot:
        #         icon = QtGui.QIcon(screenshot)
        #         item.setIcon(icon)
        #     # if name == 'screenTest (91)':
        #
        #     item.setToolTip(pprint.pformat(info))
        # # QtWidgets.QListWidgetItem('screenTest (91)').setSelected(1)
        # model_list = []
        # for ref_model in pm.ls(type=["mesh"]):
        #     model_list.append(ref_model.root().name())
        # model_list = set(model_list)
        # for i in model_list:
        #     print i
            # if i in self.library:
            #     item = QtWidgets.QListWidgetItem(i)
            #     self.listWidget2.addItem(item)

    def populate2(self):
        # search
        search_text = self.chose_asset_lineedit.text()
        self.listWidget.clear()
        path = self.lineEditFilePath.text()

        search = search_text  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "description"
        # print search
        payload = {inputfiled: search, 'key': 0}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text
        # dog = r.text
        # cat = r.json()
        # print '8'*100
        # print cat, type(cat), '<<<<<<<<<r.json>>>cat'
        # print cat[0]
        # print '8' * 100
        for i in r.json():
            # print i
            # print i['pic_name']  # pic
            screenshot = i['pic_name']
            # print i['file_name']  # file_name
            name = i['name']
            try:
                item = QtWidgets.QListWidgetItem(name)  # 添加QListWidget元素
                self.listWidget.addItem(item)
                if screenshot:
                    icon = QtGui.QIcon(screenshot)
                    item.setIcon(icon)
                    item.setToolTip(i['file_name'])
                    self.library_sql[name] = i['file_name']
            except:
                pass

                # if os.path.isdir(path):
                #     pass
                # else:
                #     path = os.path.dirname(path)
                # self.library.find(directory=path)
                # for name, info in self.library.items():
                #     try:
                #         print info['asset_catgory']
                #         if search_text in info['asset_catgory']:
                #             print 100
                #         # if search_text in name:
                #             item = QtWidgets.QListWidgetItem(name)
                #             self.listWidget.addItem(item)
                #             self.tool_list.append(name)
                #
                #             screenshot = info.get('screenshot')
                #             if screenshot:
                #                 icon = QtGui.QIcon(screenshot)
                #                 item.setIcon(icon)
                #             # if name == 'screenTest (91)':
                #             item.setToolTip(pprint.pformat(info))
                #     except:
                #         pass

    def populate3(self, pid=None):
        # tree  refreshListWidget

        search = pid
        inputfiled = "pid"
        # print search
        payload = {inputfiled: search, 'key': 0}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        for i in r.json():
            screenshot = i['pic_name']
            name = i['name']
            try:
                item = QtWidgets.QListWidgetItem(name)  # 添加QListWidget元素
                self.listWidget.addItem(item)
                if screenshot:
                    icon = QtGui.QIcon(screenshot)
                    item.setIcon(icon)
                    item.setToolTip(i['file_name'])
                    self.library_sql[name] = i['file_name']
            except:
                pass

    def add(self):
        pass

    def edit(self):
        pass

    def remove(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    # def reject(self):
    #     pass

    def accept(self):
        pass

    def ref_something(self, one):
        if not (one in self.ref_item):
            # print one, type(one)
            self.ref_item.append(one)
            newFileName = self.library.load(str(one))
            # print 'newFileName>>>', newFileName
            # cmds.file(newFileName, r=True, ns='ref')
            pm.createReference(newFileName)

    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        self.lineEditFileName.setText(fileName)
        if os.path.isfile(filePath):
            filePath = os.path.dirname(filePath)
        self.lineEditFilePath.setText(filePath)
        self.populate()

    def get_sql(self, id=0, name=''):
        #
        # print 1
        search = int(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search, 'key': 1}  #
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

    def listItemRightClicked(self, QPos):
        self.listMenu = QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("Ref Item")
        menu_item2 = self.listMenu.addAction("Remove Item")
        menu_item3 = self.listMenu.addAction("pic view")
        # self.connect(menu_item, QtCore.Signal("triggered()"), self.menuItemClicked)
        menu_item.triggered.connect(self.menuItemClicked)
        menu_item2.triggered.connect(self.menuItemClicked2)
        menu_item3.triggered.connect(self.pic_view)
        parentPosition = self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def listItemRightClicked2(self, QPos):
        self.listMenu = QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("Ref Item")
        menu_item2 = self.listMenu.addAction("Remove Item")
        # self.connect(menu_item, QtCore.Signal("triggered()"), self.menuItemClicked)
        menu_item.triggered.connect(self.menuItemClicked)
        menu_item2.triggered.connect(self.menuItemClicked2)
        parentPosition = self.listWidget2.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def menuItemClicked(self):
        currentItemName = str(self.listWidget.currentItem().text())
        # print(currentItemName)
        ma_filePath = self.library_sql[currentItemName]
        ref_ed = pm.createReference(ma_filePath, namespace='dragon')
        self.ref_ed_obj[currentItemName] = ref_ed

    def menuItemClicked2(self):
        currentItemName = str(self.listWidget.currentItem().text())
        # print('removed llll')
        # ma_filePath = self.library_sql[currentItemName]
        # pm.createReference(ma_filePath, namespace='cat')

        ref_file = self.ref_ed_obj[currentItemName]
        path = ref_file.path
        # cmds.referenceQuery(currentItemName, isNodeReferenced=True)
        # path = mc.referenceQuery(currentItemName, filename=True)
        topRef = cmds.referenceQuery(path, referenceNode=True, topReference=True)
        topPath = cmds.referenceQuery(topRef, filename=True)
        cmds.file(topPath, rr=1)

    def sql_back(self, search_info, inputfiled):
        # search info from sql
        search = search_info  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = inputfiled  # 现在能查询5个字段值{id name description,path,pid}

        all = 'id'
        if search == '':
            inputfiled = all  # 现在能查询5个字段值{id name description,path,pid}
            accurate = 0
        else:
            inputfiled = inputfiled

        if inputfiled in ['pid', 'id']:
            accurate = 1
        elif inputfiled in ['description']:
            accurate = 0

        all_list = []

        payload = {inputfiled: search, 'key': accurate}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text
        # print r.json()
        for i in r.json():
            # print i['name'], i['id']
            sub_list = (i['pid'], i['name'], i['id'])
            all_list.append(sub_list)
        return all_list

    def sql_add(pid=None, name=None, pic_path=None, file_path=None, description=None, project_name=None,
                face_num=None, producer=None):
        # add data

        if pic_path is None:
            return
        hot = pid

        file_path = os.path.normpath(file_path).replace('\\', '/')
        pic_path = os.path.normpath(pic_path).replace('\\', '/')

        payload = {'id': hot, 'name': name, 'pic_name': pic_path, 'file_name': file_path,
                   'description': description,
                   'project_name': project_name, 'face_num': face_num, 'producer': producer}
        r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
        # print r.text

    def on_treeview_clicked3(self):

        self.listWidget.clear()

        # print 'on_treeview_clicked3'
        item = self.tree.currentItem()
        # currentItem = currentIndex.internalPointer()
        filename = item.text(0)

        # print filename, type(filename), '    <<<filename<<<<<<<<'
        # print self.sql_dict
        a = self.sql_dict
        search_id = 0
        for k, v in a.items():
            # print k
            if k == filename:
                print v, '<><<<<<<<v'
                search_id = v
                self.current_pid = v

        info = self.sql_back(search_id, 'pid')
        print info, '<<<<<<info'

        self.populate3(search_id)

    def inset_sql(self):
        current_pid = self.current_pid
        # pid = "3"  # id的为所要增加的pid，必填字段
        name = self.lineEditFileName.text()
        # pic_path = r"Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat.jpg"
        # pic_path = os.path.normpath(pic_path).replace('\\', '/')
        file_path = self.lineEditFilePath.text()
        file_path = os.path.normpath(file_path).replace('\\', '/')

        name_file = os.path.basename(file_path)
        pic_name = name_file.split('.')[0]
        pic_name = pic_name + '.jpg'
        pic_path = os.path.dirname(file_path) + '/' + pic_name
        # print pic_path

        description = self.description_lineedit.text()
        project_name = self.project_combox.currentText()
        face_num = "5000"
        producer = "刘德华"
        payload = {'id': current_pid, 'name': name, 'pic_name': pic_path, 'file_name': file_path,
                   'description': description,
                   'project_name': project_name, 'face_num': face_num, 'producer': producer}
        r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)

    def pic_view(self):
        currentItemName = str(self.listWidget.currentItem().text())
        ma_filePath = self.library_sql[currentItemName]
        path = ma_filePath.replace('.ma', '.jpg')
        os.system(path)


mayaWindow = pm.ui.Window('MayaWindow')
mayaQtWindow = mayaWindow.asQtObject()

def main():
   app = QtWidgets.QApplication.instance()
   if not app:
       app = QtWidgets.QApplication(sys.argv)
   ex = MainWidget()
   ex.setParent(mayaQtWindow)
   ex.setWindowFlags(QtCore.Qt.Window)
   ex.show()
main()



if __name__ == "__main__":
    app=QApplication(sys.argv)
    main=MainWidget()
    main.show()
    app.exec_()