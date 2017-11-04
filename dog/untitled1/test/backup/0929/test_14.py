# -*- coding:utf-8 -*-
# dbtest.py
# just used for a mysql test
'''''
Created on 2012-2-12

@author: ken
'''
# mysqldb
import time, MySQLdb, sys

# connect
db = MySQLdb.connect(host="127.0.0.1", port = 3306, user="root", passwd="mw123", db="mw_dog", charset="utf8")
cursor = db.cursor()
f = open("ab.txt", "r")
i = 1
for eachline in f:
    sql = "INSERT INTO mw_table1(id, quanwen) VALUES (%d, \'%s\')" % (i, eachline)
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
       i += 1
    except:
       # Rollback in case there is any error
       db.rollback()

# 关闭数据库连接
cursor.close()
db.close()
f.close()

