# tree model
import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class TreeWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        self.setWindowTitle('TreeWidget')
        # self.tree = QtWidgets.QTreeWidget(self)

        model = QtGui.QStandardItemModel()
        parentItem = model.invisibleRootItem()
        for i in range(4):
            item = QtGui.QStandardItem("item %d" % i)
            parentItem.appendRow(item)
            parentItem = item

        treeView = QtWidgets.QTreeView(self)
        treeView.setModel(model)
        treeView.clicked[QtCore.QModelIndex].connect(self.clicked)

        self.setCentralWidget(treeView)

    def clicked(self, index):
        item = myStandardItemModel.itemFromIndex(index)
        # Do stuff with the item ...







        # self.tree.addTopLevelItem(root)


# app = QtWidgets.QApplication(sys.argv)
# app.aboutToQuit.connect(app.deleteLater)
# tp = TreeWidget()
# tp.show()
# app.exec_()

tp = TreeWidget()
tp.show()

