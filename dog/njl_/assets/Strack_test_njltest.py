# -*- coding: utf-8 -*-
# author : mengwei
# description : 资产库

import sys
import os
import re
import pprint
import requests
import logging
import platform

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from maya import OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pm
# import MyTimer
import helpform
import qrc_resources
import upload
import Updatedata_inf
import screenshots
import controllerLibraryte
reload(controllerLibraryte)
# reload(qrc_resources)

__version__ = "1.0.0"

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


class ThumbListWidget(QtWidgets.QListWidget):
    addfile = QtCore.Signal(str)
    dropped = QtCore.Signal(int, int)
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
        self.playblast_filename=""
        self.dropped.connect(self.items_dropped)

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
        else:
            event.setDropAction(QtCore.Qt.CopyAction)
        self._dropping = True
        super(ThumbListWidget, self).dropEvent(event)
        self._dropping = False

    def setCopyAction(self):
        print 'copy'

    def setMoveAction(self):
        print 'move'

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
                self.takeItem(self.row(item))
                # menu = QtWidgets.QMenu(self)
                # menu.addAction("&Del ref", self.setDelAction)
                # if menu.exec_(QtGui.QCursor.pos()):
                #     print 1

    def setDelAction(self):
        pm.undoInfo(openChunk=True)
        for item in self.selectedItems():
            ref_name = item.text()
            print ref_name, "<<<<<<<<<<<<<<<<<<<<<"
            layer_name = unicode(ref_name)
            pm.select(ref_name)
            ref_name = pm.selected()[0].name()

            cmds.referenceQuery(ref_name, isNodeReferenced=True)
            path = cmds.referenceQuery(ref_name, filename=True)
            topRef = cmds.referenceQuery(path, referenceNode=True, topReference=True)
            topPath = cmds.referenceQuery(topRef, filename=True)
            cmds.file(topPath, rr=1)
            self.takeItem(self.row(item))
        pm.undoInfo(closeChunk=True)

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
    """
    import sys
    sys.path.append(r'C:\Users\jack\PycharmProjects\untitled1\test_1')
    import pyqtlayout26_03
    reload(pyqtlayout26_03)
    """

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.sql_dict = {}  # {filename:id}
        self.buildUI()
        self.tool_list = []
        self.populate()
        self.ref_item = []
        self.ref_file = ''
        self.library_sql = {}
        self.ref_ed_obj = {}
        self.current_pid = ''
        self.info_labelfind=""
        self.pic_size = 128

        self.setWindowTitle((u"QKT AssetsLIB"))

    def buildUI(self):

        self.sizeLabel = QtWidgets.QLabel()
        self.sizeLabel.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        # menu

        fileNewAction = self.createAction("&New...", self.fileNew,
                                          QtGui.QKeySequence.New, "filenew", "Create an image file")
        fileOpenAction = self.createAction("&Open...", self.fileNew,
                                           QtGui.QKeySequence.Open, "fileopen",
                                           "Open an existing image file")
        fileSaveAction = self.createAction("&Save", self.fileNew,
                                           QtGui.QKeySequence.Save, "filesave", "Save the image")
        fileSaveAsAction = self.createAction("Save &As...",
                                             self.fileNew, icon="filesaveas",
                                             tip="Save the image using a new name")
        filePrintAction = self.createAction("&Print", self.fileNew,
                                            QtGui.QKeySequence.Print, "fileprint", "Print the image")
        fileQuitAction = self.createAction("&Quit", self.fileNew,
                                           "Ctrl+Q", "filequit", "Close the application")
        editInvertAction = self.createAction("&Invert",
                                             self.fileNew, "Ctrl+I", "editinvert",
                                             "Invert the image's colors", True, "toggled(bool)")
        editSwapRedAndBlueAction = self.createAction(
            "Sw&ap Red and Blue", self.fileNew,
            "Ctrl+A", "editswap",
            "Swap the image's red and blue color components",
            True, "toggled(bool)")
        editZoomAction = self.createAction("&Zoom...", self.fileNew,
                                           "Alt+Z", "editzoom", "Zoom the image")
        mirrorGroup = QtWidgets.QActionGroup(self)
        editUnMirrorAction = self.createAction("&Unmirror",
                                               self.setSizeMid, "Ctrl+U", "editunmirror",
                                               "Unmirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editUnMirrorAction)
        editMirrorHorizontalAction = self.createAction(
            "Mirror &Horizontally", self.setSizeBig,
            "Ctrl+H", "editmirrorhoriz",
            "Horizontally mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorHorizontalAction)
        editMirrorVerticalAction = self.createAction(
            "Mirror &Vertically", self.setSizeSmall,
            "Ctrl+V", "editmirrorvert",
            "Vertically mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorVerticalAction)
        editUnMirrorAction.setChecked(True)
        helpAboutAction = self.createAction("&About Image Changer",
                                            self.helpAbout)
        helpHelpAction = self.createAction("&Help", self.helpHelp,
                                           QtGui.QKeySequence.HelpContents)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                                fileSaveAction, fileSaveAsAction, None,
                                filePrintAction, fileQuitAction)
        # self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editInvertAction,
                                   editSwapRedAndBlueAction, editZoomAction))
        mirrorMenu = editMenu.addMenu(QtGui.QIcon(":/editmirror.png"),
                                      "&Mirror")
        self.addActions(mirrorMenu, (editUnMirrorAction,
                                     editMirrorHorizontalAction, editMirrorVerticalAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editInvertAction,
                                      editSwapRedAndBlueAction, editUnMirrorAction,
                                      editMirrorVerticalAction,
                                      editMirrorHorizontalAction))
        self.zoomSpinBox = QtWidgets.QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomSpinBox.valueChanged[int].connect(self.setPicSize)
        editToolbar.addWidget(self.zoomSpinBox)

        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchLineEdit.setPlaceholderText(u"搜索...")
        self.searchLineEdit.setToolTip("Searching")
        self.searchLineEdit.setMaximumWidth(200)
        self.searchLineEdit.returnPressed.connect(self.populate2)
        editToolbar.addWidget(self.searchLineEdit)

        # self.addActions(self.imageLabel, (editInvertAction,
        #                                   editSwapRedAndBlueAction, editUnMirrorAction,
        #                                   editMirrorVerticalAction, editMirrorHorizontalAction))

        self.resetableActions = ((editInvertAction, False),
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))

        settings = QtCore.QSettings("MyCompany", "MyApp")
        self.recentFiles = settings.value("RecentFiles")
        self.restoreGeometry(
            QtCore.QByteArray(settings.value("MainWindow/Geometry")))
        self.restoreState(QtCore.QByteArray(settings.value("MainWindow/State")))

        # menu above

        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)

        self.tree = QtWidgets.QTreeWidget()
        # tree
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels([u'分类', ''])

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

        self.tree.setItemsExpandable(True)

        mainSplitter.addWidget(self.tree)

        rightSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        self.listWidget = ThumbListWidget(self)
        self.listWidget2 = ThumbListWidget(self)

        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.listItemRightClicked)
        self.listWidget.itemDoubleClicked.connect(self.openImage)

        self.listWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget2.customContextMenuRequested.connect(self.listItemRightClicked2)

        self.listWidget2.addfile.connect(self.ref_something)

        rightSplitter.addWidget(self.listWidget)
        rightSplitter.addWidget(self.listWidget2)

        size = 128
        buffer = 12
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        self.listWidget.setDragEnabled(True)
        self.listWidget.itemClicked .connect(self.info_populate)

        self.listWidget2.setIconSize(QtCore.QSize(size, size))
        self.listWidget2.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget2.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        self.listWidget2.setDragEnabled(True)

        mainSplitter.setStretchFactor(1, 20)
        rightSplitter.setStretchFactor(0, 5)

        self.setCentralWidget(mainSplitter)

       #停靠窗口 1
        dock4=QtWidgets.QDockWidget((u"上传"),self)
        dock4.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        #dock4.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        te1=upload.UpLoad()
        dock4.setWidget(te1)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock4)

        #停靠窗口 4
        dock1=QtWidgets.QDockWidget((u"详细信息"),self)
        dock1.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
       # self.info_label = QtWidgets.QLabel((u"NULL"))
        self.info_label =Updatedata_inf.UpDatedata()
        #print str(self.info_labelfind)
        self.info_label.find(id=1)
        dock1.setWidget(self.info_label)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock1)

        #停靠窗口 2
        dock2=QtWidgets.QDockWidget((u"libraryUI"),self)
        dock2.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        #dock2.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetClosable)
        # dock2.setTitleBarWidget()
        #te2=controllerLibraryte.showUI()
        te2=screenshots.Screenshot()
        dock2.setWidget(te2)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock2)

        #停靠窗口 3
        # dock3=QtWidgets.QDockWidget((u"停靠窗口 3"),self)
        # dock3.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        # te3=QtWidgets.QTextEdit((u"窗口 3,可在 Main Window 任意位置停靠，可浮动，可关闭"))
        # dock3.setWidget(te3)
        # self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,dock3)

        #dock4 和dock1 合并
        self.tabifyDockWidget(dock4, dock1)
        #self.tabifyDockWidget(dock4, dock1 )

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None and signal == "triggered()":
            action.triggered.connect(slot)
        if slot is not None and signal == "toggled(bool)":
            action.toggled[bool].connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def fileNew(self):
        pass

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def populate(self):
        pass

    def populate2(self):
        # search
        search_text = self.searchLineEdit.text()
        self.listWidget.clear()
        # path = self.lineEditFilePath.text()

        search = search_text  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "description"
        payload = {inputfiled: search, 'key': 0}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        for i in r.json():
            screenshot = i['pic_name']
            id = i['id']
            name = i['name'] + '_' + id
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

    def populate3(self, pid=None):
        # 点击tree item 刷新列表
        size = self.pic_size
        search = pid
        inputfiled = "pid"
        # print search
        payload = {inputfiled: search, 'key': 0}
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        for i in r.json():
            screenshot = i['pic_name']
            if not os.path.isfile(screenshot):
                screenshot = r"Q:\rig\scripts\test\q_repos\aas_scripts\aas_mayaTools\ani_scripts\strack_asset\images\th.jpg"
            id = i['id']
            name = i['name']+'_'+id
            print id, '<<id,listWidget'
            try:
                item = QtWidgets.QListWidgetItem(name)  # 添加QListWidget元素
                self.listWidget.addItem(item)
                if screenshot:
                    icon = QtGui.QIcon(screenshot)
                    item.setIcon(icon)
                    item.setToolTip(i['file_name'])
                    self.library_sql[name] = i['file_name']
                self.listWidget.setIconSize(QtCore.QSize(size, size))
                buffer = 12
                self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
            except:
                pass

    def info_populate(self, item):
        """
        refresh info label
        Args:
            item:

        Returns:

        """
        item_name = item.text()

        id = item_name.split("_")[-1]
        search_info = id
        inputfiled = 'id'
        info_list = self.sql_back(search_info, inputfiled)
        # print info_list[0][-1]
        # info = info_list[0][-1]
        print item_name.split("_")[-1]
        self.info_label.find(id=item_name.split("_")[-1])      #传值给updatadata类
       #self.info_label.setText("<b>Description: %s<br>Name: %s</b><br>File Size: Null"\
       # % (info, item_name))

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

    def accept(self):
        pass

    def ref_something(self, one):
        if not (one in self.ref_item):
            self.ref_item.append(one)
            newFileName = self.library.load(str(one))
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
        search = int(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search, 'key': 1}  #
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)

        root_name = {}
        for i in r.json():
            name_a = i['name']
            id = i['id']
            root_name[name_a] = id
        return root_name

    def listItemRightClicked(self, QPos):
        """
        第一个列表的右键菜单
        Args:
            QPos:

        Returns:

        """
        self.listMenu = QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("导入Maya(参考)")
        menu_item_import = self.listMenu.addAction("导入Maya")
        menu_item2 = self.listMenu.addAction(u"删除参考")
        menu_item3 = self.listMenu.addAction("打开图片")
        menu_item_openFolder = self.listMenu.addAction("打开文件夹")

        menu_item.triggered.connect(self.menuItemClicked)
        menu_item2.triggered.connect(self.menuItemClicked2)
        menu_item3.triggered.connect(self.pic_view)
        menu_item_import.triggered.connect(self.menuItemClicked_import)
        menu_item_openFolder.triggered.connect(self.menuItemClicked_openfolder)
        parentPosition = self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def listItemRightClicked2(self, QPos):
        """
        第二个列表的右键菜单
        Args:
            QPos:

        Returns:

        """
        self.listMenu = QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("导入Maya(参考)")
        menu_item_import = self.listMenu.addAction("导入Maya")
        menu_item2 = self.listMenu.addAction(u"删除参考")
        menu_item3 = self.listMenu.addAction("打开图片")
        menu_item_openFolder = self.listMenu.addAction("打开文件夹")

        menu_item.triggered.connect(self.menuItemClicked)
        menu_item2.triggered.connect(self.menuItemClicked2)
        menu_item3.triggered.connect(self.pic_view)
        menu_item_import.triggered.connect(self.menuItemClicked_import)
        menu_item_openFolder.triggered.connect(self.menuItemClicked_openfolder)
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
        """
        导入ref
        Returns:

        """
        currentItemName = str(self.listWidget.currentItem().text())

        ref_file = self.ref_ed_obj[currentItemName]
        path = ref_file.path
        topRef = cmds.referenceQuery(path, referenceNode=True, topReference=True)
        topPath = cmds.referenceQuery(topRef, filename=True)
        cmds.file(topPath, rr=1)

    def menuItemClicked_import(self):
        """
        import to maya
        Returns:

        """
        file_path = str(self.listWidget.currentItem().toolTip())
        print(file_path)
        self.playblast_filename=file_path
        # self.playblast_picture()
        pm.importFile(file_path)

    # def playblast_picture(self):
    #     filename=(str(self.playblast_filename))
    #     strinfo = re.compile('.ma|.mb')
    #     path= strinfo.sub('.jpg',filename)
    #     cmds.viewFit()
    #     cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    #     cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=800, height=800,
    #                    showOrnaments=False, startTime=1, endTime=1, viewer=False)
    def menuItemClicked_openfolder(self):
        """

        Returns:

        """
        file_path = str(self.listWidget.currentItem().toolTip())
        folder = os.path.dirname(file_path)

        os.startfile(folder)

    def openImage(self):
        file_path = str(self.listWidget.currentItem().toolTip())
        path = file_path.replace('.ma', '.jpg')
        os.system(path)

    def sql_back(self, search_info, inputfiled):
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
        for i in r.json():
            sub_list = (i['pid'], i['name'], i['id'], i['description'])
            all_list.append(sub_list)
        return all_list

    def sql_add(pid=None, name=None, pic_path=None, file_path=None, description=None, project_name=None,
                face_num=None, producer=None):

        if pic_path is None:
            return
        hot = pid

        file_path = os.path.normpath(file_path).replace('\\', '/')
        pic_path = os.path.normpath(pic_path).replace('\\', '/')

        payload = {'id': hot, 'name': name, 'pic_name': pic_path, 'file_name': file_path,
                   'description': description,
                   'project_name': project_name, 'face_num': face_num, 'producer': producer}
        r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)

    def on_treeview_clicked3(self):

        self.listWidget.clear()

        item = self.tree.currentItem()
        filename = item.text(0)

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
        name = self.lineEditFileName.text()
        file_path = self.lineEditFilePath.text()
        file_path = os.path.normpath(file_path).replace('\\', '/')

        name_file = os.path.basename(file_path)
        pic_name = name_file.split('.')[0]
        pic_name = pic_name + '.jpg'
        pic_path = os.path.dirname(file_path) + '/' + pic_name

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

    def menuItemClicked4(self):
        """
        Open Containing Folder...
        Returns:

        """
        pass

    def setPicSize(self, size):
        self.pic_size = size

    def setSizeMid(self):
        self.pic_size = 200

    def setSizeBig(self):
        self.pic_size = 500

    def setSizeSmall(self):
        self.pic_size = 64

    def helpAbout(self):
        # print QtCore.QT_VERSION_STR
        QtWidgets.QMessageBox.about(self, "About QKT AssetsLIB",
                          """QKT AssetsLIB v {0}

          Copyright © 2017 QKT Ltd.
                          All rights reserved.

          This application can be used to perform
                          simple image manipulations.

          Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                              __version__, platform.python_version(),
                              Qt.__version__, Qt.__version__,
                              platform.system()))

    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()


import public_ctrls


def main():
    global lt
    try:
        lt.close()
        lt.deleteLater()
    except:
        pass
    lt = MainWidget(public_ctrls.get_maya_win())
    lt.show()


if __name__ == "__main__":
    app=QApplication(sys.argv)
    main=MainWidget()
    main.show()
    app.exec_()