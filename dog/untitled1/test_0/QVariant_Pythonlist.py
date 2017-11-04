"""python列表和QVariant

http://blog.csdn.net/fengyu09/article/details/37738193

pyqt中，要给QAbstractTableModel的setData函数传递一个list参数：
[20,'00:00:19']

涉及到QVariant和list的转换。
可以使用QVariant类中的toPyObject是转换。

环境是：Python 2.7.6 pyqt4 4.8.6
有文章说是，toPyObject只能转换字符串，而且只能转换字典。

测试一下，支持数字，支持字典和列表。
"""
# coding:utf-8
from PyQt4.QtCore import QVariant

a = {2: '10', 3: '00:00:09'}
aa = QVariant(a)
b = aa.toPyObject()
print b
print(b[2], b[3])

# 分割线
print('*' * 8)

a = [20, '00:00:19']
aa = QVariant(a)
b = aa.toPyObject()
print b
print(b[0], b[1])