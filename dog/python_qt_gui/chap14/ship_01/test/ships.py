# coding=utf-8
import platform
from PyQt4.QtCore import *

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


class ShipContainer(object):
    def __init__(self, filename=QString()):
        self.filename = QString(filename)
        self.dirty = False
        self.ships = {}
        self.owners = set()
        self.countries = set()

    def __len__(self):
        return len(self.ships)

    def __iter__(self):
        for ship in self.ships.values():
            yield ship
    
    def ship(self, identity):
        return self.ships.get(identity)

    def addShip(self, ship):
        self.ships[id(ship)] = ship
        self.owners.add(unicode(ship.owner))
        self.countries.add(unicode(ship.country))
        self.dirty = True

    def inOrder(self):
        return sorted(self.ships.values())

    def inCountryOwnerOrder(self):
        def compare(a, b):
            if a.country != b.country:
                return QString.localeAwareCompare(a.country, b.country)
            if a.owner != b.owner:
                return QString.localeAwareCompare(a.owner, b.owner)
            return QString.localeAwareCompare(a.name, b.name)
        return sorted(self.ships.values(), compare)


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
        
        
        
        
    
