# -*- coding:utf-8 -*-
import requests
import os


# pid = "3"    #id的为所要增加的pid，必填字段
# name = "猫"    #必填字段
# pic_path = r"Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat.jpg"
# file_path = r"Q:\rig\scripts\Q_script\test\assets_library\Modles\sets\dhg_rbj\cat.ma"
# description = "黄猫"
# project_name = "加勒比海盗"
# face_num = "5000"
# producer = "刘德华"
# payload = {'id': pid ,'name': name ,'pic_name': pic_path,'file_name':file_path,'description':description,
#            'project_name': project_name,'face_num':face_num,'producer':producer}
# r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
# print r.text

# for i in r.json():
#    print i

# pic_path = r'Q:\rig\scripts\Q_script\test\assets_library\Modles\sets\dhg_rbj\cat.ma'
# def sql_add(pid=12, name=dog, pic_path=None, file_path=None, description=None, project_name=None, face_num=None, producer=None):
#
#     if pic_path is None:
#         return
#
#     file_path = file_path.normpath(file_path).replace('\\', '/')
#
#     payload = {'id': pid, 'name': name, 'pic_name': pic_path, 'file_name': file_path, 'description': description,
#                'project_name': project_name, 'face_num': face_num, 'producer': producer}
#     r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
#     print r.text

def run():
    pid = u'11'
    name = 'dog'
    file_path = r'Q:\rig\scripts\Q_script\test\assets_library\Modles\sets\dhg_rbj\dog.ma'
    pic_path = r'Q:\rig\scripts\Q_script\test\assets_library\Modles\sets\dhg_rbj\dog2.jpg'
    description = u'绿龙_930458u2309845903'
    project_name = 'cat'

    def sql_add(pid=None, name=None, pic_path=None, file_path=None, description=None, project_name=None, face_num=None,
                producer=None):
        # add data

        if pic_path is None:
            return

        file_path = os.path.normpath(file_path).replace('\\', '/')
        pic_path = os.path.normpath(pic_path).replace('\\', '/')

        payload = {'id': pid, 'name': name, 'pic_name': pic_path, 'file_name': file_path, 'description': description,
                   'project_name': project_name, 'face_num': face_num, 'producer': producer}
        r = requests.get('http://192.168.0.34/phpconn/add.php', params=payload)
        print r.text

    sql_add(pid=pid, name=name, file_path=file_path,pic_path=pic_path, description=description,project_name=project_name)

# run()

for i in range(100):
    run()
    print i