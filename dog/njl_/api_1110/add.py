# -*- coding:utf-8 -*-
import requests


def add(pid = "1", name = "角色"  , picture_path = "", file_path = "", description = "", project_name = "", face_num = "", producer = ""):
    payload = {'id': pid ,'name': name ,'picture_path': picture_path,'file_path':file_path,'description':description,
               'project_name': project_name,'face_num':face_num,'producer':producer}
    r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
    print(r.url)
    print r.text
    # for i in r.json():
    #    print i

picture_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.png"
file_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.ma"

add(pid="5", name="cat", picture_path=picture_path, file_path=file_path, description="111", project_name="",
    face_num="10", producer="")



