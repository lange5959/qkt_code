# MVC
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super(MyListModel, self).__init__(parent)
        self._data = [70, 90, 20, 50, 100, 99]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
                not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole:
            return str(self._data[row])
        return QVariant()


class MyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item_var = index.data(Qt.DisplayRole)
        item_str = item_var.toPyObject()

        opts = QStyleOptionProgressBarV2()
        opts.rect = option.rect
        opts.minimum = 0
        opts.maximum = 100
        opts.text = item_str
        opts.textAlignment = Qt.AlignCenter
        opts.textVisible = True
        opts.progress = int(item_str)
        QApplication.style().drawControl(
            QStyle.CE_ProgressBar, opts, painter)


app = QApplication(sys.argv)
model = MyListModel()
delegate = MyDelegate()
view = QListView()
view.setModel(model)
view.setItemDelegate(delegate)
view.show()
sys.exit(app.exec_())
