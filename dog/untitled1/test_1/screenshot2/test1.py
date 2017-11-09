import sys
from PyQt5 import QtCore, QtGui, QtWidgets,QtQuickWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQuick import *
from PyQt5.QtCore import QObject, QUrl, Qt,pyqtSlot,pyqtSignal
import pixcolor
import base64


class GraspWin(QQuickView,QObject):
    graspWinQuit = pyqtSignal()
    def __init__(self):
        super(GraspWin,self).__init__()
        self.img = QtGui.QGuiApplication.primaryScreen().grabWindow(0)
        self.img.save("123.png", "png");
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(screen)
        self.setFlags(Qt.FramelessWindowHint);
        self.setColor(QtGui.QColor(Qt.transparent));
        self.setSource(QUrl("grasp.qml"))
        self.rootContext().setContextProperty("graspwin", self)
    @pyqtSlot(str,result=str)
    def getThisColor(self,pos):
        return pixcolor.getThisColor(pos, self.img)
    @pyqtSlot()
    def closeGraspwin(self):
        self.graspWinQuit.emit()
        self.close()
    @pyqtSlot(str,str,str)
    def saveGrasp(self,datas,path,ext):
        b64datas = base64.b64decode(datas.split("base64,")[1])
        bar = QtCore.QByteArray.fromBase64(base64.b64encode(b64datas))
        qimg = QtGui.QImage.fromData(base64.b64encode(b64datas))
        qpic =QtGui.QPixmap()
        isload = qpic.loadFromData(bar,ext.upper())
        if(path != "zero"):
            bol = qpic.save(path, ext.upper())
        else:
            clipb = QApplication.clipboard()
            clipb.clear()
            clipb.setPixmap(qpic)

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    c = GraspWin()
    c.show()
    myApp.exec_()
    sys.exit()