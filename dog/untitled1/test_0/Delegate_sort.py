import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListModel(QAbstractListModel):
    def __init__(self):
        super(MyListModel, self).__init__()
        self._data = [70, 80, 90, 20]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole:
            return str(self._data[row])
        elif role == Qt.EditRole:
            return str(self._data[row])
        return QVariant()


class SortProxyModel(QSortFilterProxyModel):
    def lessThan(self, left_index, right_index):
        left_var = left_index.data(Qt.DisplayRole)
        right_var = right_index.data(Qt.DisplayRole)

        left_str = left_var.toPyObject()
        right_str = right_var.toPyObject()

        left_int = int(left_str)
        right_int = int(right_str)

        return (left_int < right_int)


app = QApplication(sys.argv)
model = MyListModel()

proxy = SortProxyModel()
proxy.setSourceModel(model)
proxy.sort(0)

view = QListView()
view.setModel(proxy)
view.show()

sys.exit(app.exec_())