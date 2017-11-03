import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(MyListModel, self).__init__(parent)
        self._data = [70, 90, 20, 50, 99, 100, 10, 59]

    def flags(self, index):
        flag = super(MyListModel, self).flags(index)
        return flag | Qt.ItemIsEditable

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
                not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole:
            return str(self._data[row])
        elif role == Qt.EditRole:
            return str(self._data[row])
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or \
                not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()
        if role == Qt.EditRole:
            value_int, ok = value.toInt()
            if ok:
                self._data[row] = value_int
                self.dataChanged.emit(index, index)
                return True
            return False
        return QVariant()


class MyEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        sbox = QSpinBox(parent)
        sbox.setRange(0, 100)
        return sbox

    def setEditorData(self, editor, index):
        item_var = index.data(Qt.DisplayRole)
        item_str = item_var.toPyObject()
        item_int = int(item_str)
        editor.setValue(item_int)

    def setModelData(self, editor, model, index):
        data_int = editor.value()
        data_var = QVariant(data_int)
        model.setData(index, data_var)


class SortProxyModel(QSortFilterProxyModel):
    def lessThan(self, left_index, right_index):
        left_var = left_index.data(Qt.DisplayRole)
        right_var = right_index.data(Qt.DisplayRole)
        left_str = left_var.toPyObject()
        right_str = right_var.toPyObject()
        left_int = int(left_str)
        right_int = int(right_str)
        return (left_int < right_int)


class FilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, src_row, src_parent):
        src_model = self.sourceModel()
        src_index = src_model.index(src_row, 0)
        item_var = src_index.data(Qt.DisplayRole)
        item_int = int(item_var.toPyObject())
        return (item_int >= 71)


app = QApplication(sys.argv)

model = MyListModel()

proxy = FilterProxyModel()
proxy.setSourceModel(model)
proxy.setDynamicSortFilter(True)

view = QListView()
view.setModel(proxy)
view.show()

sys.exit(app.exec_())
