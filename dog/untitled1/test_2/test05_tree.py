import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class TreeWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        self.setWindowTitle('TreeWidget')
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])

        root = QtWidgets.QTreeWidgetItem(self.tree)
        root.setText(0, 'root')

        child1 = QtWidgets.QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QtWidgets.QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child3 = QtWidgets.QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child4 = QtWidgets.QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, 'name4')

        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)

#
# app = QtWidgets.QApplication(sys.argv)
# app.aboutToQuit.connect(app.deleteLater)
# tp = TreeWidget()
# tp.show()
# app.exec_()


tp = TreeWidget()
tp.show()
