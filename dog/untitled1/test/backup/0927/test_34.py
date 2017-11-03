# -*- coding:utf-8 -*-
import requests, json
search="0"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="pid"  # 现在能查询5个字段值{id name description,path,pid}

payload = {inputfiled:search,'key':0}   #key=1 为精确搜索 0为模糊搜索
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
# print r.text
for i in r.json():
    print i['name']
print '*'*100
search = '0' # 搜索数据相似的名字，若不填为搜索全部
inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

payload = {inputfiled: search, 'key': 1}  #
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
# print r.text

root_name = {}
for i in r.json():
    name_a = i['name']
    print name_a
    id = i['id']
    root_name[name_a] = id
    # name_a = name_a.encode('utf-8')
    # print type(name_a)
print root_name


