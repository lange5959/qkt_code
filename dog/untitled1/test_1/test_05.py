# !/usr/bin/python
import sys
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
from PyQt4 import QtGui
arr = [[1, 0, "modle1"], [2, 1, "modle2"], [3, 1, "modle3"], [4, 2, "modle4"], [5, 0, "modle5"],[6, 2, "modle6"],[7, 0, "modle7"]]
#dict1 = {0:self.root,1:self.root1}
#[1, 0, "modle1"] id pid name

class TreeWidget(QtGui.QMainWindow):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        parent = 0
        lever = 1
        # arr = [[1, 0, "modle1"], [2, 1, "modle2"], [3, 1, "modle3"], [4, 2, "modle4"], [5, 0, "modle5"],[6, 2, "modle6"],[7, 0, "modle7"]]

        self.setWindowTitle('Tree00Widget')

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
            self.root.setText(0,'root0')
            self.myQueue.append(self.root)
        else:
            lever += 1
        for i in range(0, num):
            if i == 0:
                for j in range(0, num):
                    if arr[j][1] == parent:
                        break

            if arr[i][1] == parent:
                self.treeq=i

                self.treeq= QtGui.QTreeWidgetItem(self.myQueue[arr[i][1]])
                self.treeq.setText(0,str(arr[i][2]) )
                self.myQueue.append(self.treeq)

                self.classify(arr, arr[i][0], lever)

            if j == num - 1:
                for j in range(0, num):
                    if arr[j][1] == parent:
                       # print arr[j][1]
                        break


app = QtGui.QApplication(sys.argv)
tp = TreeWidget()
tp.show()
app.exec_()