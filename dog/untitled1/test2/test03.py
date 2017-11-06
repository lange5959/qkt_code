# -*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *
from PyQt4.QtWebKit import *


class MyListModel(QAbstractListModel):
    """
    我的第一个模型
    """
    def __init__(self,parent=None):
        super(MyListModel,self).__init__(parent)

        #这是数据
        self._data=[70,90,20,50]


        pass

    def rowCount(self, parent=QModelIndex()):
        """
        这个方法返回了数据的行数
        也就是有多少个条目得数据
        """

        return len(self._data)

    def data(self,index,role=Qt.DisplayRole):
        """
        根据当前index索引，返回当前的数据
        然后再由Qt进行渲染显示
        """

        #如果当前得索引是不活动得
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            #亦或者当前的索引值不在合理范围，即小于等于0，超出总行数
            return QVariant() #返回一个QVariant，相当与空条目

        #从索引取得当前的航号
        row=index.row()

        #如果当前角色是DisplayRole
        if role==Qt.DisplayRole:
            #返回当前行的数据
            return self._data[row]

        #如果角色不满足需求，则返回QVariant
        return QVariant()


####################################################################
def main():
    app=QApplication(sys.argv)


    #新建一个ListView
    view=QListView()
    #新建一个自定义Model
    model=MyListModel()
    #设置view的model
    view.setModel(model)


    view.show()

    sys.exit(app.exec_())
####################################################################
# class MyListModel(QAbstractListModel):
#     """
#     我的第一个模型
#     """
#     def __init__(self,parent=None):
#         super(MyListModel,self).__init__(parent)
#
#         #这是数据
#         self._data=[70,90,20,50]
#
#
#         pass
#
#     def rowCount(self, parent=QModelIndex()):
#         """
#         这个方法返回了数据的行数
#         也就是有多少个条目得数据
#         """
#
#         return len(self._data)
#
#     def data(self,index,role=Qt.DisplayRole):
#         """
#         根据当前index索引，返回当前的数据
#         然后再由Qt进行渲染显示
#         """
#
#         #如果当前得索引是不活动得
#         if not index.isValid() or not 0 <= index.row() < self.rowCount():
#             #亦或者当前的索引值不在合理范围，即小于等于0，超出总行数
#             return QVariant() #返回一个QVariant，相当与空条目
#
#         #从索引取得当前的航号
#         row=index.row()
#
#         #如果当前角色是DisplayRole
#         if role==Qt.DisplayRole:
#             #返回当前行的数据
#             return self._data[row]
#
#         #如果角色不满足需求，则返回QVariant
#         return QVariant()


####################################################################

if __name__ == "__main__":
    main()