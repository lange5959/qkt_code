# coding=utf-8

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyTreeView(QTreeWidget):

    def __init__(self):
        super(MyTreeView, self).__init__()
        self.clicked.connect(self.on_treeview_clicked2)

    def on_treeview_clicked2(self):
        print 1


class TreeWidgetss(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle('qkt_Assets')
        # 创建一个Qtree部件
        self.tree = MyTreeView()
        # 设置部件的列数为2
        self.tree.setColumnCount(2)
        # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.tree.setHeaderLabels(['Category', 'Value'])

        # 设置root为self.tree的子树，所以root就是跟节点
        root = QTreeWidgetItem(self.tree)
        # 设置根节点的名称
        root.setText(0, u'模型')

        # 为root节点设置子结点
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'characters')
        child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'props')
        child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'sets')
        child4 = QTreeWidgetItem(root)
        child4.setText(0, 'sets_ss')
        child4.setText(1, 'name4')

        self.tree.addTopLevelItem(root)
        # 将tree部件设置为该窗口的核心框架
        self.setCentralWidget(self.tree)

    def get_sql(self, id=0, name=''):
        #
        print 1
        search = int(id)  # 搜索数据相似的名字，若不填为搜索全部
        inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

        payload = {inputfiled: search, 'key': 1}  #
        r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
        # print r.text

        root_name = {}
        for i in r.json():
            name_a = i['name']
            id = i['id']
            root_name[name_a] = id
            # name_a = name_a.encode('utf-8')
            # print type(name_a)
        return root_name


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
tp = TreeWidgetss()
tp.show()
app.exec_()