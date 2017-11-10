# -*- coding: utf-8 -*-
import sys
import os
import re
import maya.cmds as cmds
import requests
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui
import pymel.core as pm
import shutil


class Screenshot(QtWidgets.QWidget):
    # 排序问题 文件重名
    def __init__(self):
        super(Screenshot, self).__init__()
        self.playblastpath = ""
        self.path = ""
        self.initUI()
        self.conn()

    def initUI(self):

        self.desciption = QtWidgets.QLabel(u'截屏信息')
        self.screenshotbtn = QtWidgets.QLabel()
        self.screenshotbtn.setFixedHeight(220)
        self.screenshotbtn.setFixedWidth(220)
        self.Message = QtWidgets.QLabel(u'')
        self.Message.setStyleSheet("color:red")
        self.UpDatedatabtn = QtWidgets.QPushButton(u'截屏', self)
        self.CancelUpDatedatabtn = QtWidgets.QPushButton(u'替换', self)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.desciption, 1, 0)
        grid.addWidget(self.screenshotbtn, 1, 1, 1, 2)
        grid.addWidget(self.Message, 2, 0,1,2)
        grid.addWidget(self.UpDatedatabtn, 3, 1)
        grid.addWidget(self.CancelUpDatedatabtn, 3, 2)
        self.setLayout(grid)
        self.setWindowTitle('UpDatedatabtn')

    def conn(self):
        self.UpDatedatabtn.clicked.connect(self.screenshot)
        self.CancelUpDatedatabtn.clicked.connect(self.ReplaceScreenshots)

    def screenshot(self):
        self.playblastpath = r"Q:\rig\scripts\test\q_repos\aas_scripts\aas_mayaTools\ani_scripts\strack_asset\midchangepic.jpg"  # 设置截图保存路径
        filename = pm.sceneName()
        if filename:
            strinfo = re.compile('.ma|.mb')
            self.path = strinfo.sub('.jpg', filename)
            cmds.viewFit()
            cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
            if os.path.exists(self.path):
                picplayblast = cmds.playblast(completeFilename=self.playblastpath, forceOverwrite=True, format='image',
                                              width=500, height=500, showOrnaments=False, startTime=1, endTime=1,
                                              viewer=False)

            else:
                picplayblast = cmds.playblast(completeFilename=self.path, forceOverwrite=True, format='image',
                                              width=500, height=500, showOrnaments=False, startTime=1, endTime=1,
                                              viewer=False)

            map = QtGui.QPixmap(picplayblast)
            self.screenshotbtn.setPixmap(map)
        else:
            self.Message.setText("<h3>请打开这个文件(注意不要导入)</h3>")

    def ReplaceScreenshots(self):
        if self.path:
            self.Message.setText("<h3>替换成功</h3>")
            shutil.copyfile(self.playblastpath, self.path)

        else:
            self.Message.setText("<h3>没有截屏不能替换</h3>")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = UpDatedatabtn()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    main()