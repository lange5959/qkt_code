# -*- coding:utf-8 -*-
import requests
# add 添加数据


def add(pid="1", name="角色", pic_name="", file_name="", description="", project_name="", face_num = "", producer = ""):

    payload = {'id': pid, 'name': name, 'pic_name': pic_name, 'file_name': file_name,'description': description,
               'project_name': project_name, 'face_num': face_num, 'producer': producer}
    r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
    print r.text
    # for i in r.json():
    #    print i


add(pid="10", name="石头", pic_name="", file_name="", description="", project_name="", face_num="", producer="")
