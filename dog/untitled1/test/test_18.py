# -*- coding: UTF-8 -*-
# 数据库插入操作
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect(host="127.0.0.1", port = 3306, user="root", passwd="mw123", db="TESTDB", charset="utf8")
# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('hot', 'dog2', 11, 'M', 564)"""
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# 关闭数据库连接
db.close()