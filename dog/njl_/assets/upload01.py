# -*- coding: utf-8 -*-
import sys
import os
import re
import requests
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class Drag_ToLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(Drag_ToLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            #print event.mimeData().urls()
            event.accept()
        else:
            super(QtWidgets.QLineEdit, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            # event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            print 1
        else:
            super(QtWidgets.QLineEdit, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.setText(str(url.toLocalFile()).decode('UTF-8').encode('GBK'))


class UpLoad(QtWidgets.QWidget):
    Columnstypes= {
        u"其他" :17,
        u"角色" :2,
        u"常见室内道具" : 3,
        u"城市模型元素" : 5,
        u"人为痕迹模型库" : 9,
        u"特效破碎替代模型库" : 11,
    }
    # 排序问题 文件重名
    def __init__(self):
        super(UpLoad, self).__init__()
        # 调用qss 样式
        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))
        self.initUI()

    def initUI(self):
        self.Classify_title = QtWidgets.QLabel(u'Classify_title')
        self.desciption = QtWidgets.QLabel(u'描述')
        self.SePicturename =Drag_ToLineEdit(self)
        self.SeFilename=Drag_ToLineEdit(self)
        self.EditDesciption= QtWidgets.QTextEdit()
        self.EditProjectname = QtWidgets.QComboBox()
        for lightType in sorted(self.Columnstypes):
            self.EditProjectname.addItem(lightType)
        self.sepicture = QtWidgets.QPushButton(u'选择图片', self)
        self.sefile = QtWidgets.QPushButton(u'选择文件', self)
        self.Message = QtWidgets.QLabel(u'')
        self.Message.setStyleSheet("color:red")
        self.upload = QtWidgets.QPushButton(u'上传', self)
        self.Cancelupload = QtWidgets.QPushButton(u'取消', self)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.Classify_title, 0, 0)
        grid.addWidget(self.EditProjectname, 0, 1,1,2)
        grid.addWidget(self.desciption, 5, 0)
        grid.addWidget(self.EditDesciption, 5, 1,1,2)
        grid.addWidget(self.sepicture, 4, 0)
        grid.addWidget(self.SePicturename, 4, 1,1,2)
        grid.addWidget(self.sefile, 3, 0)
        grid.addWidget(self.SeFilename, 3, 1,1,2)
        grid.addWidget(self.Message , 6, 0)
        grid.addWidget(self.upload, 6, 1)
        grid.addWidget(self.Cancelupload, 6, 2)
        self.setLayout(grid)
        self.setWindowTitle('UpLoad')
        self.conn()

    def conn(self):
        self.SePicturename.setFocus()
        self.SePicturename.textChanged.connect(self.PicenterThing)
        # self.connect(self.SePicturename, QtCore.SIGNAL("textChanged(QString)"), self.PicenterThing)
        # self.connect(self.sepicture, QtCore.SIGNAL('clicked()'), self.showpicDialog)
        self.sepicture.clicked.connect(self.showpicDialog)
        self.SeFilename.setFocus()
        # self.connect(self.SeFilename, QtCore.SIGNAL("textChanged(QString)"), self.FileenterThing)
        self.SeFilename.textChanged.connect(self.FileenterThing)
        # self.connect(self.sefile, QtCore.SIGNAL('clicked()'), self.showfileDialog)
        self.sefile.clicked.connect(self.showfileDialog)
        self.upload.clicked.connect(self.uploadfilepic)
        self.upload.clicked.connect(self.PicenterThing)
        self.upload.clicked.connect(self.FileenterThing)
        self.Cancelupload.clicked.connect(self.Canceluploadmk)

    def  Canceluploadmk(self):
        self.SePicturename.setText("")
        self.SeFilename.setText("")
        self.EditDesciption.setText("")

    def PicenterThing(self):
        if not os.path.exists(self.SePicturename.text()) or not str(self.SePicturename.text()).split(".")[-1] in ["jpg","png"]:
            self.SePicturename.setStyleSheet("color:red")
            self.Message.setText(u"图片不存在")
        else:
            self.SePicturename.setStyleSheet("color:white")
            self.Message.setText(u"")

    def FileenterThing(self):
        if not os.path.exists(self.SeFilename.text()):
            self.SeFilename.setStyleSheet("color:red")
            self.Message.setText(u"文件不存在")
        else:
            self.SeFilename.setStyleSheet("color:white")
            self.Message.setText(u"")

    def showfileDialog(self):
        picname=[]
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.SeFilename.setText(self.filename[0])
        strinfo = re.compile('.ma')
        picname.append(strinfo.sub('.jpg', str(self.filename[0])))
        picname.append(strinfo.sub('.png', str(self.filename[0])))
        for i in picname:
            if os.path.exists(str(i)):
                self.SePicturename.setText(str(i))
                self.PicenterThing()
                self.FileenterThing()

    def showpicDialog(self):
        self.fpicname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home','Images(*.png *jpg)')
        self.SePicturename.setText(self.fpicname[0])
        strinfo = re.compile('.jpg|.png')
        autofilename= strinfo.sub('.ma', self.fpicname[0])
        self.SePicturename.setText(str(self.fpicname[0]))
        if os.path.exists(str(autofilename)) :
            self.SeFilename.setText(str(autofilename))
            self.PicenterThing()
            self.FileenterThing()

    def uploadfilepic(self):
        if os.path.exists(self.SePicturename.text()) and os.path.exists(self.SeFilename.text()):
             pic_name=str(self.SePicturename.text())
             file_name= str(self.SeFilename.text())
             description= unicode(self.EditDesciption.toPlainText())
             a = self.EditProjectname.currentText()
             pid= self.Columnstypes.get(unicode(a))
             name=file_name.split('/')[-1]
             print name
             self.upsql( pid, name, pic_name, file_name, description)
        else:
            self.Message.setText(u"图片不存在")

    def upsql(self,pid ,name,pic_name,file_name,description):
        # pid = "2"  # id的为所要增加的pid，必填字段
        # name = "test"  # 必填字段
        # pic_name = ""
        # file_name = ""
        # description = ""
        project_name = ""
        face_num = ""
        producer = ""
        payload = {'id': pid, 'name': name, 'pic_name': pic_name, 'file_name': file_name, 'description': description,
           'project_name': project_name, 'face_num': face_num, 'producer': producer}

        r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
        returnvalue= r.json()
        if 'success' in returnvalue.keys():
            self.Message.setText(u"上传成功")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = UpLoad()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()