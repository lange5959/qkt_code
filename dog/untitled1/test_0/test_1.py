import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(MyListModel, self).__init__(parent)
        self._data = [70, 90, 20, 50]

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

app = QApplication(sys.argv)
model = MyListModel()
delegate = MyEditDelegate()

view = QListView()
view.setModel(model)
view.setItemDelegate(delegate)
view.show()
sys.exit(app.exec_())