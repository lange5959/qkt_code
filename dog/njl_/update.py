# -*- coding:utf-8 -*-
import requests, json

id="8"
name="name"
pic_name="pic_name"
file_name="file_name"
description="disdd"

payload = {'id':id,'name':name,'pic_name':pic_name,'file_name':file_name,'description':description}   # id为要增加的父id 其余所有参数不能由一个为空
r = requests.get('http://192.168.0.34/phpconn/update.php', params=payload)
print  r.text
