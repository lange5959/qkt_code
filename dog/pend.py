# coding=utf-8
# tree  web
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtWebKit import QWebFrame, QWebView, QWebElement, QWebPage, QWebSettings


class MainForm(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        listLabel = QLabel("&List")

        self.listWidget=QWebView()
        self.listWidget.load(QUrl('http://192.168.0.34/picture/index.php/Home/Index/mainmenu'))
        self.listWidget.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.listWidget.linkClicked.connect(self.slt_asset)

        self.tableWidget = QWebView()
        self.tableWidget.load(QUrl('http://192.168.0.34/picture/index.php/Home/Index/indexdisplay'))
        self.tableWidget.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.tableWidget.linkClicked.connect(self.index2)

        splitter = QSplitter(Qt.Horizontal)
        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        # widget.setMaximumWidth(200)
        splitter.addWidget(widget)
        vbox = QVBoxLayout()

        vbox.addWidget(self.tableWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        splitter.setStretchFactor(1, 1)

        self.setLayout(layout)

    def slt_asset(self,url):
        t_url_info=url.toString()
        t_info_list =t_url_info.split("/")[-1]
        urlo='http://192.168.0.34/picture/index.php/Home/Index/index2/id/'+t_info_list
        # self.tableWidget.clear()
        self.tableWidget.load(QUrl(urlo))

    def index2(self,url):
        self.tableWidget.load(QUrl(url))

app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()



