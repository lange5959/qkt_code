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
        elif role == Qt.TextColorRole and column == TEU:
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