# -*- coding:utf-8 -*-
import requests, json

search="1"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="pid"  # 现在能查询5个字段值{id name discription,path,pid}

payload = {inputfiled:search}   #
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
#print r.text
for i in r.json():
    if i['name'] == u'人物模型':
        # pass
        print i['id']
    # print i['pic_name']
    # print i['file_name']


search="2"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="pid"  # 现在能查询5个字段值{id name discription,path,pid}

payload = {inputfiled:search}   #
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
#print r.text
for i in r.json():
    print i['name']

