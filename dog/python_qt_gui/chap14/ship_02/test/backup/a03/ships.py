# coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *

NAME, OWNER, COUNTRY, DESCRIPTION, TEU = range(5)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


class Ship(object):

    def __init__(self, name, owner, country, teu=0, description=""):
        self.name = QString(name)
        self.owner = QString(owner)
        self.country = QString(country)
        self.teu = teu
        self.description = QString(description)


    def __cmp__(self, other):
        return QString.localeAwareCompare(self.name.toLower(),
                                          other.name.toLower())


class ShipTableModel(QAbstractTableModel):

    def __init__(self, filename=QString()):
        super(ShipTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.ships = []
        self.owners = set()
        self.countries = set()

    def sortByName(self):
        self.ships = sorted(self.ships)
        self.reset()

    def sortByCountryOwner(self):
        def compare(a, b):
            if a.country != b.country:
                return QString.localeAwareCompare(a.country, b.country)
            if a.owner != b.owner:
                return QString.localeAwareCompare(a.owner, b.owner)
            return QString.localeAwareCompare(a.name, b.name)
        self.ships = sorted(self.ships, compare)
        self.reset()

    def rowCount(self, index=QModelIndex()):
        return len(self.ships)

    def columnCount(self, index=QModelIndex()):
        return 5

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.ships)):
            return QVariant()
        ship = self.ships[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == NAME:
                return QVariant(ship.name)
            elif column == OWNER:
                return QVariant(ship.owner)
            elif column == COUNTRY:
                return QVariant(ship.country)
            elif column == DESCRIPTION:
                return QVariant(ship.description)
            elif column == TEU:
                return QVariant(QString("%L1").arg(ship.teu))
        elif role == Qt.TextAlignmentRole:
            if column == TEU:
                return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif role == Qt.TextColorRole and column == TEU:   # 字体颜色
            if ship.teu < 80000:
                return QVariant(QColor(Qt.black))
            elif ship.teu < 100000:
                return QVariant(QColor(Qt.darkBlue))
            elif ship.teu < 120000:
                return QVariant(QColor(Qt.blue))
            else:
                return QVariant(QColor(Qt.red))
        elif role == Qt.BackgroundColorRole:
            if ship.country in (u"Bahamas", u"Cyprus", u"Denmark",
                    u"France", u"Germany", u"Greece"):
                return QVariant(QColor(250, 230, 250))
            elif ship.country in (u"Hong Kong", u"Japan", u"Taiwan"):
                return QVariant(QColor(250, 250, 230))
            elif ship.country in (u"Marshall Islands",):
                return QVariant(QColor(230, 250, 250))
            else:
                return QVariant(QColor(210, 230, 230))
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == NAME:
                return QVariant("Name")
            elif section == OWNER:
                return QVariant("Owner")
            elif section == COUNTRY:
                return QVariant("Country")
            elif section == DESCRIPTION:
                return QVariant("Description")
            elif section == TEU:
                return QVariant("TEU")
        return QVariant(int(section + 1))

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.ships):
            ship = self.ships[index.row()]
            column = index.column()
            if column == NAME:
                ship.name = value.toString()
            elif column == OWNER:
                ship.owner = value.toString()
            elif column == COUNTRY:
                ship.country = value.toString()
            elif column == DESCRIPTION:
                ship.description = value.toString()
            elif column == TEU:
                value, ok = value.toInt()
                if ok:
                    ship.teu = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row,
                              Ship(" Unknown", " Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position,
                             position + rows - 1)
        self.ships = self.ships[:position] + \
                     self.ships[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True


def generateFakeShips():
    info = (
        (u"Emma M\u00E6rsk",
         u"M\u00E6rsk Line",
         u"Denmark",
         151687,
        u"<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
        u"<font color=green>109,000 hp</font>"),
        (u"MSC Pamela",
         u"MSC",
         u"Liberia",
         90449,
        u"Draft <font color=green>15m</font>")
    )
    for name, owner, country, teu, description in info:
        yield Ship(name, owner, country, teu, description)