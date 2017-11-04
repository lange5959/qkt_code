# -*- coding:utf-8 -*-
# dbtest.py
# just used for a mysql test
# 证明数据库成功连接的测试
'''''
Created on 2012-2-12

@author: ken
'''
# mysqldb
import time, MySQLdb, sys


# 打开数据库连接
db = MySQLdb.connect(host="127.0.0.1", port = 3306, user="root", passwd="mw123", db="TESTDB", charset="utf8")
# 使用cursor()方法获取操作游标

cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

print "Database version : %s " % data

# 关闭数据库连接
db.close()



