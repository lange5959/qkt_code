from PyQt4 import QtGui
from PyQt4 import QtCore
import sys


class DigiClock(QtGui.QLCDNumber):
    def __init__(self, parent=None):
        super(DigiClock, self).__init__(parent)

        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtCore.Qt.red)
        self.setPalette(p)

        self.dragPosition = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.5)

        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.showTime)
        timer.start(1000*3)
        self.showColon = True
        self.showTime()
        self.resize(150, 60)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        if event.button() == QtCore.Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def showTime(self):
        time = QtCore.QTime.currentTime()
        print time
        text = time.toString("hh:mm")
        if self.showColon:
            text.replace(2, 1, ":")
            self.showColon = False
        else:
            text.replace(2, 1, " ")
            self.showColon = True
        self.display(text)


app = QtGui.QApplication(sys.argv)
form = DigiClock()
form.show()
app.exec_()