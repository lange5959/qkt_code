# tree clicked, add treeItems

import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class TreeWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        self.setWindowTitle('TreeWidget')
        # tree59
        self.tree = QtWidgets.QTreeWidget()

        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])

        self.root = QtWidgets.QTreeWidgetItem(self.tree)
        self.root.setText(0, 'root')

        child1 = QtWidgets.QTreeWidgetItem(self.root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QtWidgets.QTreeWidgetItem(self.root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        self.child3 = QtWidgets.QTreeWidgetItem(self.root)
        self.child3.setText(0, 'child3')
        self.child4 = QtWidgets.QTreeWidgetItem(self.child3)
        self.child4.setText(0, 'child4')
        self.child4.setText(1, 'name4')

        self.tree.addTopLevelItem(self.root)
        self.setCentralWidget(self.tree)
        self.tree.clicked.connect(self.tree_clicked)
        self.tree.expanded.connect(self.expand)
        # self.tree.clicked(QtCore.QModelIndex).connect(self.getCurrentIndex)

    def tree_clicked(self):
        item = self.tree.currentItem()
        filename = item.text(0)
        print filename
        if filename == 'child4':
            child5 = QtWidgets.QTreeWidgetItem(self.child3)
            child5.setText(0, 'child5-1')
            child5.setText(1, 'name5-1')
        if filename == 'child3':
            # self.tree.removeItemWidget(QtWidgets.QTreeWidgetItem(self.child4),0)
            self.tree.clear()

    def getCurrentIndex(self, index):
        # QtWidgets.QMessageBox.warning(self, "treeview select",
        #                               str(index.internalPointer().itemData[0]))
        pass

    def expand(self):
        item = self.tree.currentItem()
        filename = item.text(0)
        print filename
        if filename == 'child4':
            child5 = QtWidgets.QTreeWidgetItem(self.child3)
            child5.setText(0, 'child5-1')
            child5.setText(1, 'name5-1')
        if filename == 'child3':
            # self.tree.removeItemWidget(QtWidgets.QTreeWidgetItem(self.child4),0)
            self.tree.clear()


# app = QtWidgets.QApplication(sys.argv)
# app.aboutToQuit.connect(app.deleteLater)
# tp = TreeWidget()
# tp.show()
# app.exec_()


tp = TreeWidget()
tp.show()

