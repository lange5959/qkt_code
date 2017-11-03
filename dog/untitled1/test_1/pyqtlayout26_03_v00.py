# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class SplitterWidget(QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWidget, self).__init__(parent)
        # self.setWindowTitle("Splitter")

        font = QFont(self.tr("华文行楷"), 12)
        QApplication.setFont(font)

        mainSplitter = QSplitter(Qt.Horizontal, self)

        leftText = QTextEdit(self.tr("左窗口<br>sldjflksjdklf"), mainSplitter)
        leftText.setAlignment(Qt.AlignCenter)

        rightSplitter = QSplitter(Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        upText = QTextEdit(self.tr("上窗口"), rightSplitter)
        upText.setAlignment(Qt.AlignCenter)

        bottomText = QTextEdit(self.tr("下窗口"), rightSplitter)
        bottomText.setAlignment(Qt.AlignCenter)

        mainSplitter.setStretchFactor(1, 20)
        rightSplitter.setStretchFactor(2, 1)
        # mainSplitter.setWindowTitle(self.tr("分割窗口"))

        self.setCentralWidget(mainSplitter)


class MainWidget(QMainWindow):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)
        self.setWindowTitle(self.tr("依靠窗口"))

        widget = SplitterWidget()

        self.setCentralWidget(widget)

        #停靠窗口 1
        dock1=QDockWidget(self.tr("停靠窗口 1"),self)
        dock1.setFeatures(QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        te1=QTextEdit(self.tr("窗口 1,可在 Main Window 的左部和右部停靠，不可浮动，不可关闭"))
        dock1.setWidget(te1)
        self.addDockWidget(Qt.RightDockWidgetArea,dock1)

        #停靠窗口 2
        dock2=QDockWidget(self.tr("停靠窗口 2"),self)
        dock2.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetClosable)
        # dock2.setTitleBarWidget()
        te2=QTextEdit(self.tr("窗口 2,只可浮动"))
        dock2.setWidget(te2)
        self.addDockWidget(Qt.RightDockWidgetArea,dock2)

        #停靠窗口 2
        dock4=QDockWidget(self.tr("停靠窗口 4"),self)
        dock4.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetClosable)
        te4=QTextEdit(self.tr("窗口 4,只可浮动"))
        dock4.setWidget(te4)
        self.addDockWidget(Qt.RightDockWidgetArea,dock4)

        #停靠窗口 3
        dock3=QDockWidget(self.tr("停靠窗口 3"),self)
        dock3.setFeatures(QDockWidget.AllDockWidgetFeatures)
        te3=QTextEdit(self.tr("窗口 3,可在 Main Window 任意位置停靠，可浮动，可关闭"))
        dock3.setWidget(te3)
        self.addDockWidget(Qt.BottomDockWidgetArea,dock3)

        #dock1 和dock4 合并
        self.tabifyDockWidget(dock1, dock4)


if __name__ == "__main__":
    app=QApplication(sys.argv)
    main=MainWidget()
    main.show()
    app.exec_()