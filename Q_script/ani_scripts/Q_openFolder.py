from pymel.core import *
import os
path = sceneName()

path_list = path.split('/')
path_list.pop()
path = ('\\').join(path_list)

os.system("start explorer %s" % path)