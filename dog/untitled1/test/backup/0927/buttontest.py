# -*- coding: utf-8 -*-
from mybutton import MenuButton
import sys
from PyQt4.QtCore import QTextCodec, QSize, SIGNAL
from PyQt4.QtGui import QDialog, QIcon, QHBoxLayout, QApplication

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class TestDialog(QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setFixedSize(200, 200)
        self.firMybutton = MenuButton()
        self.firMybutton.setFixedSize(QSize(100, 100))
        self.firMybutton.setIcon(QIcon("windows.png"))
        self.firMybutton.setIconSize(QSize(100, 100))
        # self.firMybutton.setText(self.tr("确萨"))
        self.connect(self.firMybutton, SIGNAL("clicked()"), self.cancel)
        myLayout = QHBoxLayout()
        myLayout.addWidget(self.firMybutton)
        self.setLayout(myLayout)

    def cancel(self):
        self.close()


app = QApplication(sys.argv)
dialog = TestDialog()
dialog.show()
app.exec_()