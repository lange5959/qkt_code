import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(MyListModel, self).__init__(parent)
        self._data = [30, 49, 10, 64]

    def rowCount(self, parnet=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
            not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole:
            return str(self._data[row])
        return QVariant()

app = QApplication(sys.argv)
model = MyListModel()
view = QListView()
view.setModel(model)
view.show()
sys.exit(app.exec_())


