# -*- coding:utf-8 -*-
import requests, json

# 显示全部数据
id = "1"
payload = {'id': id}  #删除 ：删除该节点以及其所有叶节点
r = requests.get('http://192.168.0.34/phpconn/del.php', params=payload)
print  r.json()
for i in r.json():
    print i
