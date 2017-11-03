import os
import glob
import re
path = r'D:\assets_library\Modles\sets\dhg_rbj'
# print os.listdir(path)
# for i in os.listdir(path):
#     print i.
# print glob.glob(path+'/*.jpg')

# for a,b,c in os.walk(path):
    # print c  # ['GUI2_dhg_rbj_S_MOD_wyy_A.jpg',
    # print os.path.basename(c)
    # if 'GUI2_dhg_rbj_S_MOD_wyy_A' in c[0]:
    #     print c, '<<<'
    # print type(c)
    # print c

file_list = glob.iglob(r'D:\assets_library\Modles\sets\dhg_rbj\*.jpg')


def parse_path(file_path):
    fields = re.split(r'[\/\\]+', file_path)
    if len(fields) == 6:
        _, _, project_name, _disc, _libs, category, asset_name, file_name = fields

data_list = map(parse_path, file_list)