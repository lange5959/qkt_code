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

    def flags(self, index):
        flag = super(MyListModel, self).flags(index)
        return flag | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):

        row = index.row()
        if role == Qt.EditRole:
            value_int, ok = value.toInt()
            if ok:
                self._data[row] = value_int
                self.dataChanged.emit(index, index)
                return True
            return False



class FilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, src_row, src_parent):
        src_model = self.sourceModel()
        src_index = src_model.index(src_row, 0)

        item_var = src_index.data(Qt.DisplayRole)
        item_int = int(item_var.toPyObject())

        return(item_int >= 60)



app = QApplication(sys.argv)
model = MyListModel()

proxy = FilterProxyModel()
proxy.setSourceModel(model)
proxy.setDynamicSortFilter(True)

view = QListView()
view.setModel(proxy)
view.show()

sys.exit(app.exec_())




