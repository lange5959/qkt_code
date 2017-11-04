# coding=utf-8

import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import richtextlineedit


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

    def ship(self, identity):
        return self.ships.get(identity)

    def addShip(self, ship):
        self.ships[id(ship)] = ship
        self.owners.add(unicode(ship.owner))
        self.countries.add(unicode(ship.country))
        self.dirty = True


    def removeShip(self, ship):
        del self.ships[id(ship)]
        del ship
        self.dirty = True


    def __len__(self):
        return len(self.ships)


    def __iter__(self):
        for ship in self.ships.values():
            yield ship


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


    def load(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for loading"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError, "unrecognized file type version"
            self.ships = {}
            while not stream.atEnd():
                name = QString()
                owner = QString()
                country = QString()
                description = QString()
                stream >> name >> owner >> country >> description
                teu = stream.readInt32()
                ship = Ship(name, owner, country, teu, description)
                self.ships[id(ship)] = ship
                self.owners.add(unicode(owner))
                self.countries.add(unicode(country))
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def save(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for saving"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_1)
            for ship in self.ships.values():
                stream << ship.name << ship.owner << ship.country \
                       << ship.description
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


def generateFakeShips():
    for name, owner, country, teu, description in (
(u"Emma M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
 u"<font color=green>109,000 hp</font>"),
(u"MSC Pamela", u"MSC", u"Liberia", 90449,
 u"Draft <font color=green>15m</font>"),
(u"Colombo Express", u"Hapag-Lloyd", u"Germany", 93750,
 u"Main engine, <font color=green>93,500 hp</font>"),
(u"Houston Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Features a <u>twisted leading edge full spade rudder</u>. "
 u"Sister of <i>Savannah Express</i>"),
(u"Savannah Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Sister of <i>Houston Express</i>"),
(u"MSC Susanna", u"MSC", u"Liberia", 90449, u""),
(u"Eleonora M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Hallam</i>"),
(u"Estelle M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Wells</i>"),
(u"Evelyn M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
  u"Captain <i>Byrne</i>"),
(u"Georg M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gerd M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gjertrud M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Grete M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gudrun M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gunvor M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"CSCL Le Havre", u"Danaos Shipping", u"Cyprus", 107200, u""),
(u"CSCL Pusan", u"Danaos Shipping", u"Cyprus", 107200,
 u"Captain <i>Watts</i>"),
(u"Xin Los Angeles", u"China Shipping Container Lines (CSCL)",
 u"Hong Kong", 107200, u""),
(u"Xin Shanghai", u"China Shipping Container Lines (CSCL)", u"Hong Kong",
 107200, u""),
(u"Cosco Beijing", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Hellas", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Guangzhou", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Ningbo", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Yantian", u"Costamare Shipping", u"Greece", 99833, u""),
(u"CMA CGM Fidelio", u"CMA CGM", u"France", 99500, u""),
(u"CMA CGM Medea", u"CMA CGM", u"France", 95000, u""),
(u"CMA CGM Norma", u"CMA CGM", u"Bahamas", 95000, u""),
(u"CMA CGM Rigoletto", u"CMA CGM", u"France", 99500, u""),
(u"Arnold M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Morrell</i>"),
(u"Anna M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Lockhart</i>"),
(u"Albert M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Tallow</i>"),
(u"Adrian M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>G. E. Ericson</i>"),
(u"Arthur M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496, u""),
(u"Axel M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496, u""),
(u"NYK Vega", u"Nippon Yusen Kaisha", u"Panama", 97825, u""),
(u"MSC Esthi", u"MSC", u"Liberia", 99500, u""),
(u"MSC Chicago", u"Offen Claus-Peter", u"Liberia", 90449, u""),
(u"MSC Bruxelles", u"Offen Claus-Peter", u"Liberia", 90449, u""),
(u"MSC Roma", u"Offen Claus-Peter", u"Liberia", 99500, u""),
(u"MSC Madeleine", u"MSC", u"Liberia", 107551, u""),
(u"MSC Ines", u"MSC", u"Liberia", 107551, u""),
(u"Hannover Bridge", u"Kawasaki Kisen Kaisha", u"Japan", 99500, u""),
(u"Charlotte M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Clementine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Columbine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Cornelia M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Chicago Express", u"Hapag-Lloyd", u"Germany", 93750, u""),
(u"Kyoto Express", u"Hapag-Lloyd", u"Germany", 93750, u""),
(u"Clifford M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sally M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Skagen M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sofie M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sor\u00F8 M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sovereing M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Susan M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Svend M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Svendborg M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"A.P. M\u00F8ller", u"M\u00E6rsk Line", u"Denmark", 91690,
 u"Captain <i>Ferraby</i>"),
(u"Caroline M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Carsten M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Chastine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Cornelius M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"CMA CGM Otello", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM Tosca", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM Nabucco", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM La Traviata", u"CMA CGM", u"France", 91400, u""),
(u"CSCL Europe", u"Danaos Shipping", u"Cyprus", 90645, u""),
(u"CSCL Africa", u"Seaspan Container Line", u"Cyprus", 90645, u""),
(u"CSCL America", u"Danaos Shipping ", u"Cyprus", 90645, u""),
(u"CSCL Asia", u"Seaspan Container Line", u"Hong Kong", 90645, u""),
(u"CSCL Oceania", u"Seaspan Container Line", u"Hong Kong", 90645,
 u"Captain <i>Baker</i>"),
(u"M\u00E6rsk Seville", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Santana", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sheerness", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sarnia", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sydney", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"MSC Heidi", u"MSC", u"Panama", 95000, u""),
(u"MSC Rania", u"MSC", u"Panama", 95000, u""),
(u"MSC Silvana", u"MSC", u"Panama", 95000, u""),
(u"M\u00E6rsk Stralsund", u"Blue Star GmbH", u"Liberia", 95000, u""),
(u"M\u00E6rsk Saigon", u"Blue Star GmbH", u"Liberia", 95000, u""),
(u"M\u00E6rsk Seoul", u"Blue Star Ship Managment GmbH", u"Germany",
 95000, u""),
(u"M\u00E6rsk Surabaya", u"Offen Claus-Peter", u"Germany", 98400, u""),
(u"CMA CGM Hugo", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"CMA CGM Vivaldi", u"CMA CGM", u"Bahamas", 90745, u""),
(u"MSC Rachele", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"Pacific Link", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"CMA CGM Carmen", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Don Carlos", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Don Giovanni", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Parsifal", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"Cosco China", u"E R Schiffahrt", u"Liberia", 91649, u""),
(u"Cosco Germany", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"Cosco Napoli", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"YM Unison", u"Yang Ming Line", u"Taiwan", 88600, u""),
(u"YM Utmost", u"Yang Ming Line", u"Taiwan", 88600, u""),
(u"MSC Lucy", u"MSC", u"Panama", 89954, u""),
(u"MSC Maeva", u"MSC", u"Panama", 89954, u""),
(u"MSC Rita", u"MSC", u"Panama", 89954, u""),
(u"MSC Busan", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Beijing", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Toronto", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Charleston", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Vittoria", u"MSC", u"Panama", 89954, u""),
(u"Ever Champion", u"NSB Niederelbe", u"Marshall Islands", 90449,
 u"Captain <i>Phillips</i>"),
(u"Ever Charming", u"NSB Niederelbe", u"Marshall Islands", 90449,
 u"Captain <i>Tonbridge</i>"),
(u"Ever Chivalry", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Ever Conquest", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Ital Contessa", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Lt Cortesia", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"OOCL Asia", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Atlanta", u"OOCL", u"Hong Kong", 89000, u""),
(u"OOCL Europe", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Hamburg", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Long Beach", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Ningbo", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Shenzhen", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Tianjin", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Tokyo", u"OOCL", u"Hong Kong", 89097, u"")):
        yield Ship(name, owner, country, teu, description)

