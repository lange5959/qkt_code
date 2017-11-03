# -*- coding:utf-8 -*-
import requests, json


id = "3"
name = "props"
a = 1  # 目录
a = 0  # file
if a is 1:
    pic_name="1"
    file_name="1"
    discription="1"
else:
    pic_name = "c:/sss"
    file_name = "1"
    discription = "1"

payload = {'id':id,'name':name,'pic_name':pic_name,'file_name':file_name,'description':discription}   # id为要增加的父id 其余所有参数不能由一个为空

r = requests.get('http://192.168.0.34/phpconn/update.php', params=payload)
print r.text
