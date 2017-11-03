# coding=utf-8

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import requests, json

search="0"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="pid"  # 现在能查询5个字段值{id name discription,path,pid}

payload = {inputfiled:search}   #
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
#print r.text

root_name = []
for i in r.json():
    name_a = i['name']
    # name_a = name_a.encode('utf-8')
    # print type(name_a)
    root_name.append(name_a)
# print root_name[0]
    # print i['pic_name']
    # print i['file_name']


class TreeWidget(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle('TreeWidget')
        # 创建一个Qtree部件
        self.tree = QTreeWidget()
        # 设置部件的列数为2
        self.tree.setColumnCount(2)
        # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.tree.setHeaderLabels(['Key', 'Value'])

        # 设置root为self.tree的子树，所以root就是跟节点

        root_name = self.get_sql(id=0)
        for i in range(len(root_name)):
            root = 'root_'+str(i)
            root = QTreeWidgetItem(self.tree)


            root.setText(0, root_name[i])

            # 为root节点设置子结点
            child1 = QTreeWidgetItem(root)
            child1.setText(0, 'dog')
            child1.setText(1, 'name1')
            self.tree.addTopLevelItem(root)
            # 将tree部件设置为该窗口的核心框架
            self.setCentralWidget(self.tree)

    def get_sql(self, id=0, name=''):
        #
        search = str(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search}  #
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text

        root_name = []
        for i in r.json():
            name_a = i['name']
            # name_a = name_a.encode('utf-8')
            # print type(name_a)
            root_name.append(name_a)
        return root_name

app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
tp = TreeWidget()
tp.show()
app.exec_()