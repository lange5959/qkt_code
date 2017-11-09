# coding=utf-8

import os
import sys
from PyQt5.QtCore import (QModelIndex, QVariant, Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QShortcut, QTreeView)
from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

import treeoftable


class ServerModel(treeoftable.TreeOfTableModel):
    def __init__(self, parent=None):
        super(ServerModel, self).__init__(parent)

    def data(self, index, role):
        if role == Qt.DecorationRole:
            node = self.nodeFromIndex(index)
            if node is None:
                return QVariant()
            if isinstance(node, treeoftable.BranchNode):
                if index.column() != 0:
                    return QVariant()
                filename = node.toString().replace(" ", "_")
                parent = node.parent.toString()
                if parent and parent != "USA":
                    return QVariant()
                if parent == "USA":
                    filename = "USA_" + filename
                filename = os.path.join(os.path.dirname(__file__),
                                        "flags", filename + ".png")
                pixmap = QPixmap(filename)
                if pixmap.isNull():
                    return QVariant()
                return QVariant(pixmap)
        return treeoftable.TreeOfTableModel.data(self, index, role)


class TreeOfTableWidget(QTreeView):
    activated_signal = pyqtSignal(list)

    def __init__(self, filename, nesting, separator, parent=None):
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        model = ServerModel(self)
        self.setModel(model)
        self.filename = filename
        self.nesting = nesting
        self.separator = separator

        try:
            model.load(filename, nesting, separator)
        except IOError as e:
            QMessageBox.warning(self, "Server Info - Error", str(e))
        self.activated[QModelIndex].connect(self.activate)
        # QModelIndex 双击发送信号index
        self.expanded.connect(self.expand)
        self.expand()

    def currentFields(self):
        # 一整条数据（当前选中的）
        return self.model().asRecord(self.currentIndex())
        # 返回一个列表，必须是叶子节点

    def activate(self, index):
        # 双击
        self.activated_signal.emit(self.model().asRecord(index))
        # 返回一个列表，必须是叶子节点
        # self.model().asRecord(index)

    def expand(self):
        # 自动设置适配列宽度
        print(1)
        for column in range(self.model().columnCount(
                QModelIndex())):
            self.resizeColumnToContents(column)

    def add_data(self, filename, nesting, separator):
        self.model().addinfo()


class MainForm(QMainWindow):
    def __init__(self, filename, nesting, separator, parent=None):
        super(MainForm, self).__init__(parent)
        headers = ["Country/State (US)/City/Provider", "Server", "IP"]
        if nesting != 3:
            if nesting == 1:
                headers = ["Country/State (US)", "City", "Provider",
                           "Server"]
            elif nesting == 2:
                headers = ["Country/State (US)/City", "Provider",
                           "Server"]
            elif nesting == 4:
                headers = ["Country/State (US)/City/Provider/Server"]
            headers.append("IP")

        self.treeWidget = TreeOfTableWidget(filename, nesting,
                                            separator)
        self.treeWidget.expandAll()
        self.treeWidget.model().headers = headers

        self.button = QtWidgets.QPushButton("add")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.treeWidget)
        layout.addWidget(self.button)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.button.clicked.connect(self.add_data_button)

        QShortcut(QKeySequence("Escape"), self, self.close)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)

        self.treeWidget.activated_signal[list].connect(self.activated)

        self.setWindowTitle("Server Info")
        self.statusBar().showMessage("Ready...", 5000)

    def picked(self):
        # 退出时执行
        return self.treeWidget.currentFields()

    def activated(self, fields):
        # 双击执行
        self.treeWidget.expandAll()
        self.statusBar().showMessage("*".join(fields), 60000)

    def add_data_button(self):
        self.treeWidget.model().addinfo()


app = QApplication(sys.argv)
nesting = 3
if len(sys.argv) > 1:
    try:
        nesting = int(sys.argv[1])
    except:
        pass
    if nesting not in (1, 2, 3, 4):
        nesting = 3

form = MainForm(os.path.join(os.path.dirname(__file__), "servers.txt"),
                nesting, "*")
form.resize(750, 550)
form.show()
app.exec_()
print("*".join(form.picked()))