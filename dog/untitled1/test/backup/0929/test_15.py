#coding=utf-8
import MySQLdb

db = MySQLdb.connect("IP","用户名","密码","库名",charset = 'utf8')
cursor = db.cursor()

f = open("ab.txt", "r")
i = 1000000001
for eachline in f:
    sql = "INSERT INTO 表名(id, quanwen) VALUES (%d, \'%s\')" % (i, eachline)
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
db.close()
f.close()