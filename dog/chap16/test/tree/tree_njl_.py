# -*- coding:utf-8 -*-
# 搜索
import requests
search = ""  # 搜索数据相似的名字，若不填为搜索全部 id
inputfiled = "id"  # 现在能查询5个字段值{id name description,path,pid}

payload = {inputfiled: search, 'key': 0}  # key = 1 为精确搜索 0为模糊搜索
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
# print r.text
tree_info = []
for i in r.json():
    # print i
    tree_name = i['name']
    tree_info_part = [int(i['id']), int(i['pid']), tree_name]
    tree_info.append(tree_info_part)
# print '>'*10
# print tree_info
# print '*'*100

import sys
from PyQt4 import QtGui
global arr
#dict1 = {0:self.root,1:self.root1}
#[1, 0, "modle1"] id pid name


class TreeWidget(QtGui.QMainWindow):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        parent = 0
        lever = 1
        # [id,pid,name]
        # arr = [[2, 1, "modle2"], [1, 0, "modle1"], [3, 5, "modle3"], [4, 2, "modle4"], [5, 0, "modle5"],[6, 2, "modle6"],[7, 0, "modle7"]]
        arr = tree_info
        self.num = len(arr)

        self.setWindowTitle('tree njl')

        self.tree = QtGui.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.root = QtGui.QTreeWidgetItem(self.tree)
        self.root.setText(0, 'model')

        self.myQueue = []
        self.myQueue.append(self.root)
        self.classify(arr, parent, lever)
        self.tree.addTopLevelItem(self.root)
        self.setCentralWidget(self.tree)
        # print self.myQueue
        print lever

    def classify(self, arr, parent, lever):
        # print num
        if parent == 0:
            lever = 1
            print '*'*100

            # self.myQueue.append(self.root)
        else:
            lever += 1
        for i in range(0, self.num):
            if arr[i][1] == parent:
                # self.treeitem = i
                # [id,pid,name]
                # print arr[i][2]
                # print self.myQueue[arr[i][1]]
                self.treeitem = QtGui.QTreeWidgetItem(self.myQueue[arr[i][1]])
                self.treeitem.setText(0, (arr[i][2]))
                # self.treeitem.setText(1, 'name1')

                self.myQueue.append(self.treeitem)

                self.classify(arr, arr[i][0], lever-1)
        print lever


app = QtGui.QApplication(sys.argv)
tp = TreeWidget()
tp.show()
app.exec_()