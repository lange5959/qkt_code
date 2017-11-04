# -*- coding:utf-8 -*-
import requests, json
#显示全部数据
# 增
id="19"
name="name"
pic_name="pic_name"
file_name="file_name"
beizhu="beizhu"
payload = {'id':id,'name':name,'pic_name':pic_name,'file_name':file_name,'beizhu':beizhu}   # id为要增加的父id 其余所有参数不能有一个为空
r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
print  r.json()
for i in r.json():
   print i