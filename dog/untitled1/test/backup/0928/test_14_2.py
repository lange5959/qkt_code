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
conn = MySQLdb.connect(host="127.0.0.1", port = 3306, user="root", passwd="mw123", db="mw_dog", charset="utf8")
cursor = conn.cursor()
print conn
print cursor
# add
sql = "insert into user(userid, mw_dog) values(%s, %s)"
param = (15, str(20))
n = cursor.execute(sql, param)
print n

# 更新
sql = "update user set userid=%s where mw_dog=2"
param = ("ken")
n = cursor.execute(sql, param)
print n

# 查询
n = cursor.execute("select * from user")
for row in cursor.fetchall():
    for r in row:
        print r,
print ""


cursor.close()


# 关闭
conn.close()




# # add
# sql = "insert into user(name,age) values(%s,%s)"
# param = ("tom", str(20))
# n = cursor.execute(sql, param)
# print n
#
# # 更新
# sql = "update user set name=%s where Id=9001"
# param = ("ken")
# n = cursor.execute(sql, param)
# print n
#
# # 查询
# n = cursor.execute("select * from user")
# for row in cursor.fetchall():
#     for r in row:
#         print r,
# print ""
#
# # 删除
# sql = "delete from user where name=%s"
# param = ("ted")
# n = cursor.execute(sql, param)
# print n
# cursor.close()
#
# # 关闭
# conn.close()