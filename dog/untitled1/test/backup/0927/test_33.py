# coding=utf-8
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
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
                filename = os.path.join(os.path.dirname(__file__), "flags", filename + ".png")
                pixmap = QPixmap(filename)
                if pixmap.isNull():
                    return QVariant()
                return QVariant(pixmap)
        return treeoftable.TreeOfTableModel.data(self, index, role)


class TreeOfTableWidget(QTreeView):
    def __init__(self, filename, nesting, separator, parent=None):
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QtreeView.SelectItems)
        self.setUniformRowHeights(True)
        model = ServerModel(self)
        self.setModel(model)
        try:
            model.load(filename, nesting, separator)
        except IOError as e:
            QMessageBox.warning(self, "Server Info - Error", unicode(e))
        self.connect(self, SIGNAL("activated(QModelIndex)"), self.activated)
        self.connect(self, SIGNAL("expanded(QModelIndex)"), self.expanded)
        self.expanded()

    def currentFields(self):
        return self.model().asRecord(self.currentIndex())

    def activated(self, index):
        self.emit(SIGNAL("activated"), self.model().asRecord(index))

    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)


class MainForm(QMainWindow):
    def __init__(self, filename, nesting, separator, parent=None):
        super(MainForm, self).__init__(parent)
        headers = ["Country/State (US)/City/Provider", "Server", "IP"]
        if nesting != 3:
            if nesting == 1:
                headers = ["Country/State(US)", "City", "Provider", "Server"]
            elif nesting == 2:
                headers = ["Country/State (US)/City", "Provider", "Server"]
            elif nesting == 4:
                headers = ["Country/State (US)/City/Provider/Server", ]
            headers.append("IP")

        self.treeWidget = TreeOfTableWidget(filename, nesting, separator)
        self.treeWidget.model().headers = headers
        self.setCentralWidget(self.treeWidget)

        QShortcut(QKeySequence("Escape"), self, self.close)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)

        self.connect(self.treeWidget, SIGNAL("activated"), self.activated)

        self.setWindowTitle("Server Info")
        self.statusBar().showMessage("Ready...", 5000)

    def activated(self, fields):
        self.statusBar().showMessage("*".join(fields), 60000)

    def picked(self):
        return self.treeWidget.currentFields()


app = QApplication(sys.argv)
nesting = 3
if len(sys.argv) > 1:
    try:
        nesting = int(sys.argv[1])
    except:
        pass
    if nesting not in (1,2,3,4):
        nesting = 3

form = MainForm(os.path.join(os.path.dirname(__file__), "servers.txt"), nesting, "*")

form.resize(750, 550)
form.show()
app.exec_()



