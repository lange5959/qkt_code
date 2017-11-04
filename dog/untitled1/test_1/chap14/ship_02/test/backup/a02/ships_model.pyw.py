import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ships

MAC = "qt_mac_set_native_menubar" in dir()

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = ships.ShipTableModel(QString("ships.dat"))

        tableLabel1 = QLabel("Table &1")
        self.tableView1 = QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)

        tableLabel2 = QLabel("Table &2")
        self.tableView2 = QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)

        addShipButton = QPushButton("&Add Ship")
        removeShipButton = QPushButton("&Remove Ship")
        quitButton = QPushButton("&Quit")

        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)
            quitButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)

        splitter = QSplitter(Qt.Horizontal)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        # for tableView in (self.tableView1, self.tableView2):
        #     header = tableView.horizontalHeader()
        #     self.connect(header, SIGNAL("sectionClicked(int)"),
        #                  self.sortTable)

        # self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        # self.connect(removeShipButton, SIGNAL("clicked()"),
        #              self.removeShip)
        # self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Ships (model)")
        QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        if not QFile.exists(self.model.filename):
            for ship in ships.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(unicode(ship.owner))
                self.model.countries.add(unicode(ship.country))
            self.model.reset()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError, e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: %s" % e)
        self.model.sortByName()













app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()