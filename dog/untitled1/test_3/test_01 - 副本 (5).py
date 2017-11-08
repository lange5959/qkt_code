from PySide import QtGui, QtCore
import sys

class SI(object):

    # children = []

    def __init__(self, group=None, parent=None):
        self.parent = parent
        self.group = group
        self.children = []

    def data(self, column):
        return self.group[column]

    def appendChild(self, group):
        self.children.append(SI(group, self))

    def child(self, row):
        return self.children[row]

    def childrenCount(self):
        return len(self.children)

    def hasChildren(self):
        if len(self.children) > 0 :
            return True
        return False

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0

    def columnCount(self):
        return len(self.group)

class SM(QtCore.QAbstractItemModel):

    root = SI(["First", "Second"])

    def __init__(self, parent=None):
        super(SM, self).__init__(parent)
        self.createData()

    def createData(self):
        for x in [["a", "A"], ["b","B"], ["c", "C"]]:
            self.root.appendChild(x)
        for y in [["a1", "AA"], ["a2", "AB"], ["a3","AC"]]:
            self.root.child(0).appendChild(y)

    def columnCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        else:
            return self.root.columnCount()

    def rowCount(self, index=QtCore.QModelIndex()):
        if index.row() > 0:
            return 0
        if index.isValid():
            item = index.internalPointer()
        else:
            item = self.root
        return item.childrenCount()

    def index(self, row, column, index=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, index):
            return QtCore.QModelIndex()
        if not index.isValid():
            item = self.root
        else:
            item = index.internalPointer()

        child = item.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QtCore.QMOdelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        item = index.internalPointer()
        if not item:
            return QtCore.QModelIndex()

        parent = item.parent
        if parent == self.root:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(parent.row(), 0, parent)

    def hasChildren(self, index):
        if not index.isValid():
            item = self.root
        else:
            item = index.internalPointer()
        return item.hasChildren()

    def data(self, index, role=QtCore.Qt.DisplayRole):
       if index.isValid() and role == QtCore.Qt.DisplayRole:
            return index.internalPointer().data(index.column())
       elif not index.isValid():
            return self.root.getData()

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.root.data(section)

class MyTree(QtGui.QTreeView):
    def __init__(self, parent=None, model=SM):
        super(MyTree, self).__init__(parent)
        self.setModel(model())


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.initGui()

    def initGui(self):
       vlo = QtGui.QVBoxLayout()
       tree = MyTree(self)
       vlo.addWidget(tree)
       self.setLayout(vlo)
       self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    exit(app.exec_())

if __name__ == '__main__':
    main()