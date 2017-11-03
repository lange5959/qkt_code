# coding=utf-8
import requests, json


def get_sql(id=0, name=''):
    #
    search = str(id)  # 搜索数据相似的名字，若不填为搜索全部
    inputfiled = "pid"  # 现在能查询5个字段值{id name discription,path,pid}

    payload = {inputfiled: search}  #
    r = requests.get('http://192.168.0.34/phpconn/find.php', params=payload)
    # print r.text

    root_name = {}
    for i in r.json():
        # print i['name']
        name_a = i['name']
        id = i['id']
        root_name[name_a] = id
        # name_a = name_a.encode('utf-8')
        # print type(name_a)
    return root_name

print get_sql(id=0)
# get_sql(id=0)