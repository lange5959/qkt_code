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
    tree_name = i['name']
    tree_info_part = [int(i['id']), int(i['pid']), tree_name]
    tree_info.append(tree_info_part)
print tree_info

import sys
from PyQt4 import QtGui
arr = tree_info
#dict1 = {0:self.root,1:self.root1}
#[1, 0, "modle1"] id pid name


class TreeWidget(QtGui.QMainWindow):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        parent = 0
        lever = 1
        # arr = [[1, 0, "modle1"], [2, 1, "modle2"], [3, 1, "modle3"], [4, 2, "modle4"], [5, 0, "modle5"],[6, 2, "modle6"],[7, 0, "modle7"]]


        self.setWindowTitle('tree_nie')

        self.myQueue = []
        self.classify(arr, parent, lever)
        print self.myQueue
        self.tree.addTopLevelItem(self.root)
        self.setCentralWidget(self.tree)

    def classify(self, arr, parent, lever):

        num = len(arr)
        # print num
        if parent == 0:
            lever = 1
            self.tree = QtGui.QTreeWidget()
            self.root = QtGui.QTreeWidgetItem(self.tree)
            self.root.setText(0, u'模型')
            self.myQueue.append(self.root)
        else:
            lever += 1
        for i in range(0, num):

            if arr[i][1] == parent:
                self.treeq=i

                self.treeq= QtGui.QTreeWidgetItem(self.myQueue[arr[i][1]])
                self.treeq.setText(0, (arr[i][2]))
                self.myQueue.append(self.treeq)

                self.classify(arr, arr[i][0], lever)

            # if j == num - 1:
            #     for j in range(0, num):
            #         if arr[j][1] == parent:
            #            # print arr[j][1]
            #             break


app = QtGui.QApplication(sys.argv)
tp = TreeWidget()
tp.show()
app.exec_()