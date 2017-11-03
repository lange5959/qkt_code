# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from PyQt4.QtNetwork import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class TcpClient(QDialog):
    def __init__(self, parent=None):
        super(TcpClient, self).__init__(parent)
        self.setWindowTitle(self.tr("测试tcp"))

        self.status = False
        self.serverIP = QHostAddress()
        self.port = 8010
        self.msglist = QByteArray()

        vbMain = QVBoxLayout(self)
        self.ListWidgetContent = QListWidget(self)
        vbMain.addWidget(self.ListWidgetContent)

        hb = QHBoxLayout()
        self.LineEditMessage = QLineEdit(self)
        hb.addWidget(self.LineEditMessage)
        self.PushButtonSend = QPushButton(self)
        self.PushButtonSend.setText(self.tr("添加"))
        self.PushButtonSend.setEnabled(False)
        hb.addWidget(self.PushButtonSend)
        self.connect(self.PushButtonSend, SIGNAL("clicked()"), self.slotSend)

        hb1 = QHBoxLayout()
        LabelName = QLabel(self)
        LabelName.setText(self.tr("用户名:"))
        self.LineEditUser = QLineEdit(self)
        hb1.addWidget(LabelName)
        hb1.addWidget(self.LineEditUser)

        # hb2 = QHBoxLayout()
        # LabelServerIP = QLabel(self)
        # LabelServerIP.setText(self.tr("服务器地址:"))
        # self.LineEditIP = QLineEdit(self)
        # hb2.addWidget(LabelServerIP)
        # hb2.addWidget(self.LineEditIP)

        # hb3 = QHBoxLayout()
        # LabelPort = QLabel(self)

        # LabelPort.setText(self.tr("端口:"))
        # self.LineEditPort = QLineEdit(self)
        # hb3.addWidget(LabelPort)
        # hb3.addWidget(self.LineEditPort)


        vbMain.addLayout(hb)
        vbMain.addLayout(hb1)
        # vbMain.addLayout(hb2)
        # vbMain.addLayout(hb3)

        self.PushButtonLeave = QPushButton(self)
        self.PushButtonLeave.setText(self.tr("开始"))
        vbMain.addWidget(self.PushButtonLeave)

        self.connect(self.PushButtonLeave, SIGNAL("clicked()"), self.slotEnter)

    def slotSend(self):
        msg = self.userName + ":" + self.LineEditMessage.text()
        length = self.tcpSocket.writeData(msg.toUtf8())
        self.LineEditMessage.clear()
        if length != msg.toUtf8().length():
            return

    def slotEnter(self):
        if not self.status:
            ip = "127.0.0.1"  # self.LineEditIP.text()
            if not self.serverIP.setAddress(ip):
                QMessageBox.information(self, self.tr("error"), self.tr("server ip address error!"))
                return
            if self.LineEditUser.text() == "":
                QMessageBox.information(self, self.tr("error"), self.tr("User Name error!"))
                return
            self.userName = self.LineEditUser.text()
            self.tcpSocket = QTcpSocket(self)
            self.connect(self.tcpSocket, SIGNAL("connected()"), self.slotConnected)
            self.connect(self.tcpSocket, SIGNAL("disconnected()"), self.slotDisconnected)
            self.connect(self.tcpSocket, SIGNAL("readyRead()"), self.dataReceived)
            self.tcpSocket.connectToHost(self.serverIP.toString(), 8010)
            self.status = True
        else:
            msg = self.userName + ":" + self.tr("结束")
            length = self.tcpSocket.writeData(msg.toUtf8())
            if length != msg.toUtf8().length():
                return
            self.tcpSocket.disconnectFromHost()
            self.status = False

    def slotConnected(self):
        self.PushButtonSend.setEnabled(True)
        self.PushButtonLeave.setText(self.tr("结束"))

        msg = self.userName + ":" + self.tr("开始")
        length = self.tcpSocket.writeData(msg.toUtf8())
        if length != msg.toUtf8().length():
            return

    def slotDisconnected(self):
        self.PushButtonSend.setEnabled(False)
        self.PushButtonLeave.setText(self.tr("开始"))

    def dataReceived(self):
        while self.tcpSocket.bytesAvailable() > 0:
            length = self.tcpSocket.bytesAvailable()
            msg = QString(self.tcpSocket.read(length))
            msg = msg.fromUtf8(msg)
            self.ListWidgetContent.addItem(msg.fromUtf8(msg))


app = QApplication(sys.argv)
dialog = TcpClient()
dialog.show()
app.exec_()