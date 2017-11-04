# -*- coding:utf-8 -*-


import requests
search = "30"  # 搜索数据相似的名字，若不填为搜索全部 30
inputfiled = "pid"  # 现在能查询5个字段值{id name description, path, pid}

payload = {inputfiled: search, 'key': 1}   # key=1 为精确搜索 0 为模糊搜索
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)

# print r.text

for i in r.json():
    # print i
    print i['id'], i['name'], i['pic_name']
