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
