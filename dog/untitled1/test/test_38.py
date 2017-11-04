# -*- coding:utf-8 -*-
# import requests, json
# #insert data
# id="1"
# name="characters"
# pic_path="xxx"
# file_path="xxx"
# description="xxx"
# payload = {'id':id,'name':name,'pic_name':pic_path,'file_name':file_path,'description':description}   # id为要增加的父id 其余所有参数不能有一个为空
# r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
# print  r.json()
# for i in r.json():
#    print i


import requests
# insert data


id = "2"  #'pid'
name = "cat"
pic_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.png"
file_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.ma"
description = "一只猫，黑猫，丑猫"
payload = {'id': id, 'name': name, 'pic_name': pic_path, 'file_name': file_path, 'description':description}
# id为要增加的父id 其余所有参数不能有一个为空
r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
print r.json()

for i in r.json():
   print i