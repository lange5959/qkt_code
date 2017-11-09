# -*- coding: utf-8 -*-
from  PyQt4 import QtCore, QtGui
from  Screenshot import Ui_ScrShot
import sys
# import icoqrc


class MainFrom(QtGui.QWidget):
    def __init__(self):
        super(MainFrom, self).__init__()
        self.Ui = Ui_ScrShot()
        self.Ui.setupUi(self)
        self.Ui.labelShow.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)  # size 策略为 可扩展 expanding
        self.Ui.labelShow.setAlignment(QtCore.Qt.AlignCenter)  # alignment 对齐方式 居中
        self.Ui.labelShow.setMinimumSize(240, 160)  # 最小为 240 X 160
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 设置总是在最前
        self.setWindowTitle(u'截图工具')
        self.setWindowIcon(QtGui.QIcon(':qq.ico'))

        self.shootScreen()
        self.Ui.spinBox.setSuffix(' s')
        self.Ui.spinBox.setMaximum(60)
        self.Ui.spinBox.setValue(5)

        self.Ui.pushButtonNew.clicked.connect(self.newScreenshot)  # 从新开始新建截图
        self.Ui.pushButtonSave.clicked.connect(self.saveScreenshot)  # 保存截图
        self.Ui.pushButton_Quit.clicked.connect(self.close)  # 退出

    # 截图
    def shootScreen(self):
        if self.Ui.spinBox.value() != 0:
            QtGui.qApp.beep()  # 操作带上系统的响铃
        self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())  # 获取 屏幕桌面截图
        self.updateScreenshotLabel()
        self.Ui.pushButtonNew.setDisabled(False)
        if self.Ui.checkBoxHideThis.isChecked():  # 当选择隐藏按钮为True时， 截图完成显示窗体
            self.show()


            #  获取图片显示在label上

    def updateScreenshotLabel(self):
        # self.originalPixmap.scaled()  scaled()函数的声明const返回一个Qpixmap
        # QtCore.Qt.KeepAspectRatio 尽可能大的在一个给定的矩形大小缩放到一个矩形且保持长宽比。
        # QtCore.Qt.SmoothTransformation 平滑转换
        self.Ui.labelShow.setPixmap(self.originalPixmap.scaled(self.Ui.labelShow.size(), QtCore.Qt.KeepAspectRatio,
                                                               QtCore.Qt.SmoothTransformation))

        # 保存截图图片

    def saveScreenshot(self):
        format = 'png'
        initialPath = QtCore.QDir.currentPath() + "/untitled." + format

        fileName = QtGui.QFileDialog.getSaveFileName(self, u"另存为",
                                                     initialPath,
                                                     "%s Files (*.%s)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)

            # 新创建截图

    def newScreenshot(self):
        if self.Ui.checkBoxHideThis.isChecked():
            self.hide()
        self.Ui.pushButtonNew.setDisabled(True)
        QtCore.QTimer.singleShot(self.Ui.spinBox.value() * 1000, self.shootScreen)  # * 秒后触发截图

    # 重载 resizeEvent 方法
    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.Ui.labelShow.size(), QtCore.Qt.KeepAspectRatio)
        if not self.Ui.labelShow.pixmap() or scaledSize != self.Ui.labelShow.pixmap().size():  # 当pixmap改变大小时候重新加载updateScreenshotLabel
            self.updateScreenshotLabel()


if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    MainApp = MainFrom()
    MainApp.show()
    sys.exit(App.exec_())