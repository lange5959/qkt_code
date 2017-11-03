# coding:utf-8

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class KUnit:
    # 调试类
    @staticmethod
    def run(name, C):
        if name == "__main__":
            import sys
            app = QApplication(sys.argv)

            obj = C()
            obj.show()
            sys.exit(app.exec_())


class KTabBar(QTabBar):
    # 自定义tabbar,实现双击关闭
    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)

    def mouseDoubleClickEvent(self, event):
        # 获取点击的tab
        tabId = self.tabAt(event.pos())
        # 发送关闭信号和tabid
        self.emit(SIGNAL("tabCloseRequested(int)"), self.tabAt(event.pos()))

        QTabBar.mouseDoubleClickEvent(self, event)


class MyDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout(self)
        self.setFixedSize(QSize(500, 500))
        self.tabwidget = QTabWidget()
        layout.addWidget(self.tabwidget)

        # 设置tabwidget的bar
        self.tabwidget.setTabBar(KTabBar())
        # 允许tab点击关闭
        self.tabwidget.setTabsClosable(True)

        self.tabwidget.addTab(QDialog(), "tab1")
        self.tabwidget.addTab(QDialog(), "tab2")
        self.tabwidget.addTab(QDialog(), "tab3")
        self.tabwidget.addTab(QDialog(), "tab4")
        self.tabwidget.addTab(QDialog(), "tab5")
        # 连接信号槽
        self.connect(self.tabwidget, SIGNAL("tabCloseRequested(int)"), self.closeTab)

    def closeTab(self, tabId):
        # 关闭置顶信号槽
        self.tabwidget.removeTab(tabId)


KUnit.run(__name__, MyDialog)