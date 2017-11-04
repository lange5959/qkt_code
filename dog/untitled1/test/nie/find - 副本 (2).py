# -*- coding:utf-8 -*-
import requests
import json

search="猫"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="description"  # 现在能查询5个字段值{id name description,path,pid}


all = 'id'
if search == '':
    inputfiled = all  # 现在能查询5个字段值{id name description,path,pid}
    accurate = 0
else:
    inputfiled = inputfiled

if inputfiled in ['pid']:
    accurate = 1
elif inputfiled in ['description']:
    accurate = 0



payload = {inputfiled:search ,'key':accurate}
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
# print r.text
# print r.json()
for i in r.json():
    print i['name']
