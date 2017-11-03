# coding=utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ship_w

MAC = "qt_mac_set_native_member" in dir()


class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        listLabel = QLabel("&List")
        self.listWidget = QListWidgt()
        listLabel.setBuddy(self.listWidget)

        tableLabel = QLabel("&Table")
        self.tableWidget = QTableWidget()
        tableLabel.setBuddy(self.treeWidget)

        treeLabel = QLabel("Tre&e")
        self.treeWidget = QTreeWidget()
        treeLabel.setBuddy(self.treeWidget)

        addShipButton = QPushButton("&Add Ship")
        removeShipButton = QPushButton("&Remove Ship")
        quitButton = QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)

        splitter = QSpliter(Qt.Horizontal)
        vbox = QVBoxLayout()
        vbox.addWidget(listLabel)
        vbox.addWidget(self.listWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel)
        vbox.addWidget(self.tableWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        vbox = QVBoxLayout()
        vbox.addWidget(treeLabel)
        vbox.addWidget(self.treeWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)

        layout = QVBoxLayout()
        layout.addwidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(self.tableWidget, SIGNAL("itemChanged(QTableWidgetItem*"), self.tableItemChanged)

        self.ships = ship_w.ShipContainer(QString("ship.dat"))
        self.setWindowTitle("Ship (dict)")
        QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        if not QFile.exists(self.ships.filename):
            for ship in ship_w.generateFakeShips():
                self.ships.addShip(ship)
            self.ships.dirty = False
        else:
            try:
                self.ships.load()
            except IOError, e:
                QMessageBox.warning(self, "Ships - Error",
                                    "Failed to load: %s" % e)
        self.populateList()
        self.populateTable()
        self.tableWidget.sortItems()
        self.populateTree()

    def addShip(self):
        ship = ship_w.Ship(" Unknown", " Unknown", " Unknown")
        self.ships.addShip(ship)  # 添加资产
        self.populateList()
        self.populateTree()
        self.populateTable(id(ship))
        self.tableWidget.setFocus()
        self.tableWidget.editItem(self.tableWidget.currentItem())

    def populateList(self, selectedShip=None):
        selected = None
        self.listWidget.clear()
        for ship in self.ships.inOrder():
            item = QListWidgetItem(QString("%1 of %2/%3 (%L4)")\
                                   .arg(ship.name).arg(ship.owner).arg(ship.country)\
                                   .arg(ship.teu))
            self.listWidget.addItem(item)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.listWidget.setCurrentItem(selected)

    def populateTable(self, selectedShip=None):
        selected = None
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(self.ships))
        headers = ["Name", "Owner", "Country", "Description", "TEU"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        for row, ship in enumerate(self.ships):
            item = QTableWidgetItem(ship.name)
            item.setData(Qt.UserRole, QVariant(long(id(ship))))  # ?
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.tableWidget.setItem(row, ship_w.NAME, item)
            self.tableWidget.setItem(row, ship_w.OWNER, QTableWidgetItem(ship.owner))
            self.tableWidget.setItem(row, ship_w.COUNTRY, QTableWidgetItem(ship.COUNTRY))
            self.tableWidget.setItem(row, ship_w.DESCRIPTION, QTableWidgetItem(ship.description))
            item = QTableWidgetItem(QString('%L1')\
                                    .arg(ship.teu, 8, 10, QChar(" ")))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.tableWidget.setItem(row, ships.TEU, item)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnCountents()
        if selected is not None:
            selected.setSelected(True)
            self.tableWidget.setCurrentItem(selected)





















