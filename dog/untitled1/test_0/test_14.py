import sys
import glob
import re

strack_api_path = r"\\DESKTOP-VC4Q511\strack_api_release\latest\strack_api"
if strack_api_path not in sys.path:
    sys.path.append(strack_api_path)

import strack

# reload(strack)

login = "mengwei"
api_key = "0ac32bd32b0a3c69eccc5443f23d0b9d"

st = strack.Strack(base_url="http://192.168.120.65/strack_task/public",
                   login=login, api_key=api_key)

project_name = "Cosmos Laundromat"

category_map = {
    "props": "Prop",
    "chars": "Character",
    "envs": "Environment"
}


def parse_path(file_path):
    fields = re.split(r'[\/\\]+', file_path)
    if len(fields) == 8:
        _, _, project_name, _disc, _libs, category, asset_name, file_name = fields
    elif len(fields) == 9:
        _, _, project_name, _disc, _libs, category, _othersheep, asset_name, file_name = fields
    else:
        return
    fields = file_name.split(".")
    if len(fields) == 3:
        step = fields[1]
    else:
        step = None
    return {"project_name": project_name,
            "category": category,
            "asset_name": asset_name,
            "file_name": file_name,
            "step": step
            }


file_list = glob.iglob(r'\\DESKTOP-J2B8UL2\Cosmos Laundromat\Disc2\libs\*\*\*.blend')

data_list = map(parse_path, file_list)

project = st.project.find("name = %s" % project_name)

for i in data_list:
    asset_name = i["asset_name"]

    if not asset_name:
        continue
    category_name = category_map.get(i["category"])

    if not category_name:
        continue
    category = st.category.find("name=%s" % category_name)
    if not category:
        print category_name
        continue

    if not st.asset.find("name=%s" % asset_name):
        new_asset = st.asset.create(
            data={"name": asset_name, "project_id": project.get("id"), "category_id": category.get("id")})
        print "creating new asset", new_asset
    else:
        print "%s is already exists" % asset_name

st.category.find()