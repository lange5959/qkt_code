# -*- coding: utf-8 -*-
import sys
import os
import requests
from Qt import QtCore
from Qt import QtWidgets


class UpDatedata(QtWidgets.QWidget):


    Columnstypes= {
        u"自然环境元素": 10,
        u"其他": 17,
        u"角色": 2,
        u"常见室内道具": 3,
        u"城市模型元素": 5,
        u"人为痕迹模型库": 9,
        u"特效破碎替代模型库": 11,
    }

    def __init__(self):
        super(UpDatedata, self).__init__()
        # 调用qss 样式
        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))
        self.all_list = []
        self.initUI()
        self.conn()

    def initUI(self):
        self.Classify_title = QtWidgets.QLabel(u'分类')
        self.desciption = QtWidgets.QLabel(u'描述信息')
        self.SePicturename =QtWidgets.QLineEdit()
        self.SeFilename=QtWidgets.QLineEdit()
        self.EditDesciption= QtWidgets.QTextEdit()
        self.EditClassify= QtWidgets.QComboBox()
        for Classify in sorted(self.Columnstypes):
            self.EditClassify.addItem(Classify)
        self.sepicture = QtWidgets.QLabel(u'图片地址')
        self.sefile = QtWidgets.QLabel(u'文件地址')
        self.Message = QtWidgets.QLabel(u'')
        self.Message.setStyleSheet("color:red")
        self.UpDatedata = QtWidgets.QPushButton(u'更新', self)
        self.CancelUpDatedata = QtWidgets.QPushButton(u'取消', self)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.Classify_title, 0, 0)
        grid.addWidget(self.EditClassify, 0, 1,1,2)
        grid.addWidget(self.desciption, 5, 0)
        grid.addWidget(self.EditDesciption, 5, 1,1,2)
        grid.addWidget(self.sepicture, 4, 0)
        grid.addWidget(self.SePicturename, 4, 1,1,2)
        grid.addWidget(self.sefile, 3, 0)
        grid.addWidget(self.SeFilename, 3, 1,1,2)
        grid.addWidget(self.Message , 6, 0)
        grid.addWidget(self.UpDatedata, 6, 1)
        grid.addWidget(self.CancelUpDatedata, 6, 2)
        self.setLayout(grid)
        self.setWindowTitle('UpDatedata')

    def conn(self):
        self.UpDatedata.clicked.connect(self.UpdData)
        self.CancelUpDatedata.clicked.connect(self.cancedata)

    def find(self, id=None):
        # 从数据库搜索
        if id:
            try:
               search = id  # 搜索数据相似的名字，若不填为搜索全部
               inputfiled ="id" # 现在能查询5个字段值{id name description,path,pid}
               payload = {inputfiled: search, 'key': 1}
               r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
               self.all_list = []
               for i in r.json():
                   sub_list = [i['pid'], i['name'], i['pic_name'], i['file_name'], i['description'],i['id']]
                   self.all_list.append(sub_list)
               self.SePicturename.setText(str(self.all_list[0][2]))
               self.SeFilename.setText(str(self.all_list[0][3]))
               self.EditDesciption.setText(self.all_list[0][4])
               comboxsort =[u"人为痕迹模型库", u"其他", u"城市模型元素", u"常见室内道具", u"自然环境元素", u"特效破碎替代模型库", u"角色"]
               for (key, value) in self.Columnstypes.items():
                   if value==int(self.all_list[0][0]):
                       GetIndex=comboxsort.index(key)
                       self.EditClassify.setCurrentIndex(GetIndex)
            except:
                self.Message.setText("未获得数据库正确回复")

    def UpdData(self):
        pic_name = str(self.SePicturename.text())
        file_name = str(self.SeFilename.text())
        description = unicode(self.EditDesciption.toPlainText())
        classnamed = self.EditClassify.currentText()
        pid = self.Columnstypes.get(unicode(classnamed))
        name = file_name.split('/')[-1]
        id=self.all_list[0][5]
        #print name, pid, pic_name, file_name,description
        self.requsestsql(pid, name, pic_name, file_name, description, id)

    def requsestsql(self, pid, name, pic_name, file_name, description, id):
        if not id or not name:
            pass
        else:
            print pid, name, pic_name, file_name, description, id
            payload = {'id': id, 'pid': pid, 'name': name, 'pic_name': pic_name, 'file_name': file_name, 'description': description}
            r = requests.get('http://192.168.0.34/phpconn/update.php', params=payload)
            print r.text

    def cancedata(self):
        pass

def main():
        app = QtWidgets.QApplication(sys.argv)
        ex = UpDatedata()
        ex.show()
        sys.exit(app.exec_())
if __name__ == '__main__':
    main()