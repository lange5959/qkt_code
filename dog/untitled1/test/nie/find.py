# -*- coding:utf-8 -*-
import requests

# search="2"  #搜索数据相似的名字，若不填为搜索全部
# inputfiled="id"  # 现在能查询5个字段值{id name description,path,pid}
#
#
# all = 'id'
# if search == '':
#     inputfiled = all  # 现在能查询5个字段值{id name description,path,pid}
#     accurate = 0
# else:
#     inputfiled = inputfiled
#
# if inputfiled in ['pid', 'id']:
#     accurate = 1
# elif inputfiled in ['description']:
#     accurate = 0
#
#
# payload = {inputfiled:search ,'key':accurate}
# r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
# print type(r)
# # print r.text
# # print r.json()
# for i in r.json():
#     print i['name'], i['id']


def sql_back(search_info, inputfiled):
    search = search_info  # 搜索数据相似的名字，若不填为搜索全部
    inputfiled = inputfiled  # 现在能查询5个字段值{id name description,path,pid}

    all = 'id'
    if search == '':
        inputfiled = all  # 现在能查询5个字段值{id name description,path,pid}
        accurate = 0
    else:
        inputfiled = inputfiled

    if inputfiled in ['pid', 'id']:
        accurate = 1
    elif inputfiled in ['description']:
        accurate = 0

    all_list = []

    payload = {inputfiled: search, 'key': accurate}
    r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
    # print r.text
    # print r.json()
    for i in r.json():
        # print i['name'], i['id']
        sub_list = (i['pid'], i['name'], i['id'])
        all_list.append(sub_list)
    return all_list


# search="1"
# inputfiled="pid"
# sql_info = sql_back(search, inputfiled)
# print sql_info
# # [('1','model'),()]
# for i in sql_info:
#     print i[1], i[2]




