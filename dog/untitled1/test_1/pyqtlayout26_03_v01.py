# -*- coding: utf-8 -*-

import sys
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
# QtCore.QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class SplitterWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWidget, self).__init__(parent)

        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)

        leftText = QtWidgets.QTextEdit((u"左窗口<br>sldjflksjdklf"), mainSplitter)
        leftText.setAlignment(QtCore.Qt.AlignCenter)

        rightSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        upText = QtWidgets.QTextEdit((u"上窗口"), rightSplitter)
        upText.setAlignment(QtCore.Qt.AlignCenter)

        bottomText = QtWidgets.QTextEdit((u"下窗口"), rightSplitter)
        bottomText.setAlignment(QtCore.Qt.AlignCenter)

        mainSplitter.setStretchFactor(1, 20)
        rightSplitter.setStretchFactor(2, 1)
        # mainSplitter.setWindowTitle(("分割窗口"))

        self.setCentralWidget(mainSplitter)


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)
        self.setWindowTitle((u"依靠窗口"))

        widget = SplitterWidget()

        self.setCentralWidget(widget)

        #停靠窗口 1
        dock1=QtWidgets.QDockWidget((u"停靠窗口 1"),self)
        dock1.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        te1=QtWidgets.QTextEdit((u"窗口 1,可在 Main Window 的左部和右部停靠，不可浮动，不可关闭"))
        dock1.setWidget(te1)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock1)

        #停靠窗口 2
        dock2=QtWidgets.QDockWidget((u"停靠窗口 2"),self)
        dock2.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetClosable)
        # dock2.setTitleBarWidget()
        te2=QtWidgets.QTextEdit((u"窗口 2,只可浮动"))
        dock2.setWidget(te2)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock2)

        #停靠窗口 2
        dock4=QtWidgets.QDockWidget((u"停靠窗口 4"),self)
        dock4.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetClosable)
        te4=QtWidgets.QTextEdit((u"窗口 4,只可浮动"))
        dock4.setWidget(te4)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock4)

        #停靠窗口 3
        dock3=QtWidgets.QDockWidget((u"停靠窗口 3"),self)
        dock3.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        te3=QtWidgets.QTextEdit((u"窗口 3,可在 Main Window 任意位置停靠，可浮动，可关闭"))
        dock3.setWidget(te3)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,dock3)

        #dock1 和dock4 合并
        self.tabifyDockWidget(dock1, dock4)


if __name__ == "__main__":
    app=QApplication(sys.argv)
    main=MainWidget()
    main.show()
    app.exec_()