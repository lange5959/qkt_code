# -*- coding:utf-8 -*-
import requests, json


def updatesql(update_id=None, pid=None, name="", picture_path="", file_path="", description=""):
    if not update_id or not name:
        pass
    else:
        print  pid, name, picture_path, file_path, description, update_id
        payload = {'id': update_id, 'pid': pid, 'name': name, 'picture_path': picture_path, 'file_path': file_path,
                   'description': description}
        r = requests.get('http://192.168.0.34/phpconn/update.php', params=payload)
        print r.text

picture_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.jpg"
file_path = "Q:/rig/scripts/Q_script/test/assets_library/Modles/sets/dhg_rbj/cat2.ma"
updatesql(update_id=30, pid=5, name="cat2", picture_path=picture_path, file_path=file_path, description="xx")

