# -*- coding:utf-8 -*-
import requests

search="5"  #搜索数据相似的名字，若不填为搜索全部
inputfiled="id"  # 现在能查询5个字段值{id name description,path,pid}

payload = {inputfiled:search ,'key':1}
r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
print r.text
# print r.json()
for i in r.json():
  print '*'*10
  print i['name']
  #print binascii.a2b_hex(i).decode("utf8")