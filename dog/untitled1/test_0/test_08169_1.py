# coding=utf-8
# 定时保存
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore


app = QtGui.QApplication(sys.argv)
try:
    due = QtCore.QTime.currentTime()
    message = "Alert!"
    if len(sys.argv)<2:
        raise ValueError
    hours,mins = sys.argv[1].split(":")
    due = QtCore.QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]"

while QtCore.QTime.currentTime() < due:
    time.sleep(3)

label = QtGui.QLabel("<font color=red size=10><b>" + message + "</b></font>")
label.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
label.setWindowFlags(QtCore.Qt.SplashScreen)
label.show()
QtCore.QTimer.singleShot(60000/10, app.quit)

app.exec_()