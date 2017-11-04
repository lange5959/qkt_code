# -*- coding: UTF-8 -*-
# 创建数据库表
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect(host="127.0.0.1", port = 3306, user="root", passwd="mw123", db="TESTDB", charset="utf8")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE_2")

# 创建数据表SQL语句
sql = """CREATE TABLE EMPLOYEE_2 (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# 关闭数据库连接
db.close()