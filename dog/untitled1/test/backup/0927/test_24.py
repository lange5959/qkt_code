# -*- coding: utf-8 -*-
# mysqldb
import sys
import time, MySQLdb
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class TcpClientSocket(QTcpSocket):
    def __init__(self, parent=None):
        super(TcpClientSocket, self).__init__(parent)
        self.connect(self, SIGNAL("readyRead()"), self.dataReceive)
        self.connect(self, SIGNAL("disconnected()"), self.slotDisconnected)
        self.length = 0
        self.msglist = QByteArray()

    def dataReceive(self):
        while self.bytesAvailable() > 0:
            length = self.bytesAvailable()
            msg = self.read(length)
            self.emit(SIGNAL("updateClients(QString,int)"), msg, length)

    def slotDisconnected(self):
        pass

class Server(QTcpServer):
    def __init__(self, parent=None, port=0):
        super(Server, self).__init__(parent)
        self.listen(QHostAddress.Any, port)
        self.tcpClientSocketList = []

    def incomingConnection(self, socketDescriptor):
        tcpClientSocket = TcpClientSocket(self)
        self.connect(tcpClientSocket, SIGNAL("updateClients(QString,int)"), self.updateClients)
        self.connect(tcpClientSocket, SIGNAL("disconnetcted(int)"), self.slotDisconnected)
        tcpClientSocket.setSocketDescriptor(socketDescriptor)
        self.tcpClientSocketList.append(tcpClientSocket)

    def updateClients(self, msg, length):
        self.emit(SIGNAL("updateServer(QString,int)"), msg, length)
        for i in xrange(len(self.tcpClientSocketList)):
            item = self.tcpClientSocketList[i]
            length_msg = item.writeData(msg.toUtf8())
            if length_msg != msg.toUtf8().length():
                continue

    def slotDisconnected(self, descriptor):
        for i in xrange(len(self.tcpClientSocketList)):
            item = self.tcpClientSocketList[i]
            if item.socketDescriptor() == descriptor:
                self.tcpClientSocketList.remove[i]
                return
        return


class TcpServer(QDialog):
    def __init__(self, parent=None, f=None):
        super(TcpServer, self).__init__(parent)
        self.setWindowTitle("TCP Server")
        vbMain = QVBoxLayout(self)

        self.ListWidgetContent = QListWidget(self)
        vbMain.addWidget(self.ListWidgetContent)

        hb = QHBoxLayout()
        LabelPort = QLabel(self)
        LabelPort.setText(self.tr("Port:"))
        hb.addWidget(LabelPort)

        LineEditPort = QLineEdit(self)
        hb.addWidget(LineEditPort)

        vbMain.addLayout(hb)

        self.PushButtonCreate = QPushButton(self)
        self.PushButtonCreate.setText(self.tr("Create"))
        vbMain.addWidget(self.PushButtonCreate)

        self.connect(self.PushButtonCreate, SIGNAL("clicked()"), self.slotCreateServer)
        self.port = 8010
        LineEditPort.setText(QString.number(self.port))

    def slotCreateServer(self):
        server = Server(self, self.port)
        self.connect(server, SIGNAL("updateServer(QString,int)"), self.updateServer)
        self.PushButtonCreate.setEnabled(False)

    def updateServer(self, msg, length):
        self.ListWidgetContent.addItem(msg.fromUtf8(msg))

        db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="mw123", db="TESTDB", charset="utf8")
        cursor = db.cursor()
        tsql = msg.fromUtf8(msg)
        # msgsql=msg.fromUtf8(msg)
        print '>>>', tsql, '>>>>>type>', type(tsql)
        f = []
        message = tsql
        f = message.split('*')
        # f.append(tsql)
        i = 'dog'
        # for eachline in f:
        sql = "INSERT INTO EMPLOYEE_2(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES (\'%s\', \'%s\', %d, \'%s\', %d)" % (i, f[0], 11, f[1], 2000)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            i += 1
        except:
            # Rollback in case there is any error
            db.rollback()

        # 关闭数据库连接
        cursor.close()
        db.close()


app = QApplication(sys.argv)
dialog = TcpServer()
dialog.show()
app.exec_()